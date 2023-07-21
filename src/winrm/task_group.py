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

    def _format_error(self, hostname: str, error_message: str) -> dict:
        return {"Hostname": hostname,
                "Status": "Failure",
                "Timestamp": datetime.now().isoformat(),
                "Error Message": error_message
                }

    def _format(self, stdout: str, hostname: str, task_name: str):
        skeleton = {"Hostname": hostname,
                    "Status": "Success",
                    "Timestamp": datetime.now().isoformat(),
                    "Task Name": task_name}
        reader = csv.DictReader(stdout.split('\n')[1:])
        if len(reader) == 1:
            yield json.dumps(skeleton | reader)
        else:
            yield json.dumps(skeleton | {"Results": [row for row in reader]})

    async def _execute_task(self, user: User, host: Host) -> dict:
        success, conn, shell_id = await create_connection(host=host, user=user, transport=self.transport)
        if not success or not conn or not shell_id:
            print("Formatting Error in JSON")
            yield json.dumps({"Hostname": host.hostname,
                              "Status": "Failure",
                              "Timestamp": datetime.now().isoformat(),
                              "Error": shell_id if shell_id else "Connection Returned null"})
        else:
            for i in self.tasks:
                command_id, stdout, stderr, status = await execute_command(host,
                                                                           user,
                                                                           i.stages["Stages"][1],
                                                                           self.transport,
                                                                           conn,
                                                                           shell_id)
                # TODO: Find out why this keeps failing
                if command_id:
                    try:
                        print(f"Cleaning up command {i.name} for {host.hostname}")
                        await asyncio.get_running_loop().run_in_executor(exe, functools.partial(conn.cleanup_command, shell_id=shell_id, command_id=command_id))
                        print(f"Done cleaning command {i.name} for {host.hostname}")
                    except:
                        print("Exeception cleaning command")
                if status != 0 or len(stdout) < 5:
                    yield json.dumps(self._format_error(host.hostname, stderr))
                else:
                    print(f"Formatting results in JSON for task {i.name} related to host {host.hostname}")
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as exe:
                        yield await asyncio.get_event_loop().run_in_executor(None, functools.partial(self._format, task_name=i.name, stdout=stdout, hostname=host.hostname))
                    print(f"Done formatting results for task {i.name}")
            if shell_id:
                await asyncio.get_running_loop().run_in_executor(None, functools.partial(conn.close_shell, shell_id=shell_id))
    
    def __insert_into_db(self, value: str, handler: DBHandler, collection):
        print(f"Inserting into collection {collection}")
        if collection == "Failure":
            handler.insert(collection, json.loads(value))
        if handler.is_connected:
            handler.upsert(collection, json.loads(value))
        else:
            raise RuntimeError("Database is not connected")
        print(f"Done Inserting into collection {collection}")
    
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
                    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
                        self.__insert_into_db(value=i,
                                            handler=db_handler,
                                            collection="Hosts" if json.loads(i)["Status"] != "Failure" else "Failure"
                                            )
        if group:
            async for i in group:
                async for j in self._execute_task(user, i):
                    if debug:
                        print(j)
                    else:
                        self.__insert_into_db(j,
                                            db_handler,
                                            "Hosts" if json.loads(i)["Status"] != "Failure" else "Failure")