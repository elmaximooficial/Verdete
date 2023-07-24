from src.winrm.host_group import HostGroup
from src.winrm.windows import WinRMConnection
#from src.database.db_handler import SurrealDBHandler
from src.util.task_formatter import TaskFormatter as tf
from datetime import datetime
from winrm import Response
from collections import namedtuple
import asyncio


WinRMTask = namedtuple("WinRMTask", ["name", "script"])


class WinRMTaskGroup:
    tasks: dict
    result_skeleton: dict = {
                        "Hostname": None,
                        "Timestamp": datetime.now().isoformat(),
                    }
    
    def __init__(self, *args):
        self.tasks = {task.name: WinRMConnection.encode_command(task.script) for task in args}

    async def execute(self,
                      group: HostGroup = None,
                      debug: bool = False):
                      #db_handler: SurrealDBHandler = None):
        async with asyncio.TaskGroup() as tg:
            async with group as gp:
                while True:
                    print("Popping connection from queue")
                    connection = tg.create_task(gp.get())
                    print("Got connection from pool")
                    if connection is None:
                        break
                    for task_name, encoded in self.tasks.items():
                        print("Executing task and parsing the response")
                        response = Response(tg.create_task(connection.execute_ps(encoded)))

                        print("Cheking for Errors")
                        if response.status_code != 0:
                            self.result_skeleton["Hostname"] = connection.transport.endpoint
                            print(self.result_skeleton | {"Status": "Failure",
                                              "Task Name": task_name,
                                              "Error Code": response.std_err})
                        if debug:
                            print(self.result_skeleton | {"Status": "OK",
                                              "Task Name": task_name,
                                              "Results": tf.csv_to_dict(response.std_out)})
                        else:
                            print(self.result_skeleton | {"Status": "OK",
                                              "Task Name": task_name,
                                              "Results": tf.csv_to_dict(response.std_out)})
                            #await db_handler.upsert(collection='hosts', mode='csv',
                            #                        data=skeleton | {"Status": "OK",
                            #                                    "Task Name": task_name,
                            #                                   "Results": tf.csv_to_dict(response.std_out)})




