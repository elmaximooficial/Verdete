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
    tasks: list
    result_skeleton: dict = {
                        "Hostname": None,
                        "Timestamp": datetime.now().isoformat(),
                    }
    debug: bool
    success: dict = []

    @staticmethod
    async def fetch_task(tasks: list, **kwargs):
        task = WinRMTaskGroup(tasks=tasks, name=kwargs.get('name'))
        await task.__from_db()
        return task

    async def __from_db(self):
        async with MongoDBHandler() as handler:
            database_task_group = await handler.find_one("winrm_task_group", {"name": self.name})
            if database_task_group is None:
                await self.__create_new()
                return
            self.tasks = database_task_group['tasks']

    async def __create_new(self):
        async with MongoDBHandler() as handler:
            await handler.insert(collection='winrm_task_group', data=[{"name": self.name, "tasks": self.tasks}])

    def __init__(self, name: str, tasks: list = None):
        self.name = name
        self.tasks = []
        self.tasks.append({task.name: WinRMConnection.encode_command(task.script) for task in tasks})

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
            for i in self.tasks:
                for task_name, encoded in i.items():
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




