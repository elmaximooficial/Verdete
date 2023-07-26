from fastapi_app import app
from src.winrm.task_group import WinRMTaskGroup
from src.database.db_handler import MongoDBHandler
from src.util.task_formatter import TaskFormatter as tf


@app.get("/winrmtask")
async def get_all_task_groups():
    async with MongoDBHandler() as handler:
        task_groups = [i for i in await handler.find('winrm_task_group')]


@app.get("/winrmtask/{name}")
async def get_task_group(name: str):
    task_group = await WinRMTaskGroup.fetch_task(name)
    return {
        "name": task_group.name,
        "tasks": task_group.tasks
    }


@app.get("/winrmtask/{name}/results")
async def get_task_group_results(name: str):
    async with MongoDBHandler() as handler:
        return tf.json_to_dict(await handler.find(collection='winrm_hosts', projection={name: 1}))


@app.get("/winrmtask/{name}/results/{host}")
async def get_task_group_results_for_host(name: str, host: str):
    async with MongoDBHandler() as handler:
        return tf.json_to_dict(await handler.find(collection='winrm_hosts',
                                                  selection={'hostname': host},
                                                  projection={name: 1}))
