import concurrent.futures
from queue import Queue
from src.winrm.host import Host
from src.winrm.host_group import HostGroup
from src.util.password_manager import User
from src.util.ldap import LDAP
from src.winrm.windows import *
from src.database.db_handler import DBHandler
import json
import csv
from datetime import datetime


class TaskGroup:
    tasks: list
    transport: WINRM_TRANSPORT
    current_task: str
    
    def __init__(self, *args, transport):
        self.tasks = []
        self.transport = transport
        self.tasks.extend(iter(args))

    def _format_results(self, hostname: str, result: list) -> dict:
        raw_dict = {"Hostname": hostname, "Status": "Success", "Timestamp": datetime.now().isoformat()}
        for line in result:
            if line.strip():
                name, value = line.split('\t')
                raw_dict[name] = value
        return raw_dict

    def _format_error(self, hostname: str, error_message: str) -> dict:
        return {"Hostname": hostname,
                "Status": "Failure",
                "Timestamp": datetime.now().isoformat(),
                "Error Message": error_message
                }

    def _format(self, stdout:str, hostname: str):
        json_out = []
        reader = csv.DictReader(stdout.split('\n')[1:])
        for row in reader:
            json_out.append(row)
        yield json.dumps({"Hostname": hostname,
                          "Status": "Success",
                          "Timestamp": datetime.now().isoformat(),
                          "Results": json_out},
                         indent=2)

    async def _execute_task(self, user: User, host: Host) -> dict:
        try:
            success, conn, shell_id = await create_connection(host=host, user=user, transport=self.transport)
        except WinRMError:
            yield json.dumps({"Hostname": host.hostname, "Status": "Failure", "Timestamp": datetime.now().isoformat(), "Error": "Max Connections Exceeded"}, indent=2)
        if not success:
            print("Formatting Error in JSON")
            yield json.dumps({"Hostname": host.hostname,
                              "Status": "Failure",
                              "Timestamp": datetime.now().isoformat(),
                              "Error": shell_id},
                             indent=2)
        else:
            for i in self.tasks:
                self.current_task = i.name
                command_id, stdout, stderr, status = await execute_command(host,
                                                                           user,
                                                                           i.stages["Stages"][1],
                                                                           self.transport,
                                                                           conn,
                                                                           shell_id)
                if command_id:
                    conn.cleanup_command(shell_id, command_id)
                if status != 0 or len(stdout) < 5:
                    yield json.dumps(self._format_error(host.hostname, stderr))
                else:
                    print("Formatting results in JSON")
                    formatted = None
                    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as exe:
                        formatted = await asyncio.get_event_loop().run_in_executor(exe, functools.partial(self._format, stdout=stdout, hostname=host.hostname))
                    for i in formatted:
                        yield i
            conn.close_shell(shell_id)
    
    async def __insert_into_db(self, value: str, handler: DBHandler, collection):
        print("Inserting into DB")
        if collection == "Failure":
                await handler.insert(collection, json.loads(value))
        if handler.is_connected:
            await handler.upsert(collection, json.loads(value))
            await handler.upsert("Hosts", {"Hostname": json.loads(value)["Hostname"],
                                     "Status": json.loads(value)["Status"],
                                     "Last Communication": datetime.now().isoformat()
                                     })
        else:
            raise RuntimeError("Database is not connected")
    
    async def execute(self,
                      user: User,
                      group: HostGroup = None,
                      host: Host = None,
                      debug: bool = False,
                      db_handler: DBHandler = None):
        if host:
            async for i in self._execute_task(user, host):
                if debug:
                    print(i)
                else:
                    await self.__insert_into_db(i,
                                                db_handler,
                                                self.current_task if json.loads(i)["Status"] != "Failure" else "Failure"
                                                )
        if group:
            async for i in group:
                async for j in self._execute_task(user, i):
                    if debug:
                        print(j)
                    else:
                        await self.__insert_into_db(j,
                                                    db_handler,
                                                    self.current_task if json.loads(i)["Status"] != "Failure" else "Failure")