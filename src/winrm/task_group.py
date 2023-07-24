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

                    if connection is None:
                        break

                    skeleton = {
                        "Hostname": connection.hostname,
                        "Timestamp": datetime.now().isoformat(),
                    }
                    for task_name, encoded in self.tasks.items():
                        response = Response(tg.create_task(connection.execute_ps(encoded)))

                        if response.status_code != 0:
                            print(skeleton | {"Status": "Failure",
                                              "Task Name": task_name,
                                              "Error Code": response.std_err})
                        if debug:
                            print(skeleton | {"Status": "OK",
                                              "Task Name": task_name,
                                              "Results": tf.csv_to_dict(response.std_out)})
                        else:
                            print(skeleton | {"Status": "OK",
                                              "Task Name": task_name,
                                              "Results": tf.csv_to_dict(response.std_out)})
                            #await db_handler.upsert(collection='hosts', mode='csv',
                            #                        data=skeleton | {"Status": "OK",
                            #                                    "Task Name": task_name,
                            #                                   "Results": tf.csv_to_dict(response.std_out)})




