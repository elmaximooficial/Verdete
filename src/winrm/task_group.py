from src.winrm.host_group import HostGroup, TempHostGroup
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
    """
    This object represents a WinRM Task Group, which executes every task in 'tasks' in every connection of the group
    passed to execute(), without closing the shell in between commands
    """
    tasks: list
    result_skeleton: dict = {
                        "Hostname": None,
                        "Timestamp": datetime.now().isoformat(),
                    }
    debug: bool
    success: dict = []

    @staticmethod
    async def fetch_task(name):
        """
        Loads task group from the database
        :param name: The name of the task group to load
        :return: The task group initialized with the attributes stored in the database
        """
        task = WinRMTaskGroup(name=name)
        await task.__from_db()
        return task

    @staticmethod
    async def create_task(tasks: list, name: str):
        """
        Creates a new task group and stores into the database
        :param tasks: The list of tasks to be executed
        :param name: The name of the task group, should be unique
        :return:
        """
        task = WinRMTaskGroup(name=name)
        task.tasks = tasks
        task.__create_new()

    async def __from_db(self):
        async with MongoDBHandler() as handler:
            database_task_group = await handler.find_one("winrm_task_group", {"name": self.name})
            if database_task_group is None:
                print(f"Task Group {self.name} cannot be found on the database")
                return
            self.tasks = database_task_group['tasks']

    async def __create_new(self):
        async with MongoDBHandler() as handler:
            await handler.insert(collection='winrm_task_group', data={"name": self.name, "tasks": self.tasks})

    def __init__(self, name: str):
        """ This should not be called directly, use create_task() or fetch_task instead()"""
        self.name = name
        self.tasks = []

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
                        self.result_skeleton["Hostname"] = connection.transport.endpoint
                        print(self.result_skeleton | {"Status": "OK",
                                                      "Task Name": task_name,
                                                      "Results": await tf.csv_to_dict(response.std_out)})
                        self.success.append(connection.hostname)
                        continue
                    else:
                        self.result_skeleton["Hostname"] = connection.transport.endpoint
                        await db_handler.insert(collection='winrm_hosts',
                                                data=self.result_skeleton | {"Status": "OK",
                                                            "Task Name": task_name,
                                                           "Results": await tf.csv_to_dict(response.std_out)})
                        self.success.append(connection.hostname)
                        continue
            await connection.dispose()

    async def execute(self,
                      group: (HostGroup | TempHostGroup),
                      debug: bool = False):
        """
        Executes the task group on the 'group' paramater.
        There are two options for group, the HostGroup which is a full on HostGroup stored in the database, and the
        TempHostGroup, which is a more flexible type of HostGroup, stored in memory for how long as this task exists.
        Can be useful when executing a TaskGroup with the OnHostGroupChange trigger, which should run the TaskGroup on the
        new hosts
        :param group: The HostGroup or TempHostGroup to execute the tasks on
        :param debug: Flag indicating the debug level for the TaskGroup
        """
        self.debug = debug
        print("Created Asyncio TaskGroup")
        async with asyncio.TaskGroup() as tg:
            print("Entering HostGroup loop")
            async with MongoDBHandler() as handler:
                async for i in group:
                    tg.create_task(self.__execute_task(endpoint=i, user=group.user, db_handler=handler))
        print(f"Success: {len(self.success)} Failure: {group.size - len(self.success)}")




