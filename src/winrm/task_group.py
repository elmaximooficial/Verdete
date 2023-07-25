from src.winrm.host_group import HostGroup
from src.winrm.windows import WinRMConnection
from src.database.db_handler import MongoDBHandler
from src.util.task_formatter import TaskFormatter as tf
from datetime import datetime
from winrm import Response
from collections import namedtuple
import asyncio
import functools


WinRMTask = namedtuple("WinRMTask", ["name", "script"])


class WinRMTaskGroup:
    tasks: dict
    result_skeleton: dict = {
                        "Hostname": None,
                        "Timestamp": datetime.now().isoformat(),
                    }
    debug: bool
    success: dict = []
    
    def __init__(self, *args):
        self.tasks = {task.name: WinRMConnection.encode_command(task.script) for task in args}

    async def __execute_task(self, endpoint, user, db_handler = None):
        connection = WinRMConnection(endpoint=f"{endpoint['protocol']}://{endpoint['hostname']}:{endpoint['port']}/wsman",
                                     username=user.username,
                                     password=user.password,
                                     server_cert_validation='ignore',
                                     transport=endpoint['transport'])
        print(f"Connecting to Endpoint {endpoint}")
        await connection.connect()
        if connection.shell_id is not None:
            print("Entering TaskGroup loop")
            for task_name, encoded in self.tasks.items():
                print("Executing task")
                res = await connection.execute_ps(encoded=encoded)
                print("Parsing Response")
                response = None if res is None else Response(res)
                print("Cheking for Errors")
                if response is None or response.status_code != 0:
                    self.result_skeleton["Hostname"] = connection.transport.endpoint
                    print(self.result_skeleton | {"Status": "Failure",
                                                  "Task Name": task_name,
                                                  "Error Code": "No response" if not response else response.std_err})
                    continue
                if self.debug:
                    print(self.result_skeleton | {"Status": "OK",
                                                  "Task Name": task_name,
                                                  "Results": await tf.csv_to_dict(response.std_out)})
                    self.success.append(connection.hostname)
                    continue
                else:
                    await db_handler.insert(collection='winrm_hosts', mode='csv',
                                            data=[self.result_skeleton | {"Status": "OK",
                                                        "Task Name": task_name,
                                                       "Results": await tf.csv_to_dict(response.std_out)}])
                    self.success.append(connection.hostname)
                    continue
            await connection.dispose()
    async def execute(self,
                      group: HostGroup = None,
                      debug: bool = False):
                      #db_handler: SurrealDBHandler = None):
        self.debug = debug
        print("Created Asyncio TaskGroup")
        async with asyncio.TaskGroup() as tg:
            print("Entering HostGroup loop")
            async with MongoDBHandler() as handler:
                async for i in group:
                    tg.create_task(self.__execute_task(endpoint=i, user=group.user, db_handler=handler))
        print(f"Success: {len(self.success)} Failure: {group.size() - len(self.success)}")




