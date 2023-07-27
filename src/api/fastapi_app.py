import asyncio
import functools

from src.database.db_handler import MongoDBHandler
from src.winrm.host_group import HostGroup
from src.winrm.task_group import WinRMTaskGroup, WinRMTask
from src.util.task_formatter import TaskFormatter as tf
from src.winrm.windows import WinRMConnection
from fastapi import FastAPI, HTTPException, Header
from typing import Annotated
import threading

app = FastAPI()

@app.get('/')
async def greetings():
    return {
        "name": "Verdete",
        "description": "Network monitoring and managing software",
        "author": "Matteus Maximo Felisberto - matteusmaximof@gmail.com",
        "version": '0.0.1-alpha'
    }

################################################################################################
################################################################################################
############################################ TASKS #############################################
################################################################################################
################################################################################################

@app.get("/winrmtask")
async def get_all_task_groups():
    async with MongoDBHandler() as handler:
        task_groups = [i async for i in handler.find('winrm_task_group', projection={'_id': 0})]
        return task_groups

@app.get("/winrmtask/{name}")
async def get_task_group(name: str):
    task_group = await WinRMTaskGroup.fetch_task(name)
    if len(task_group.tasks) == 0:
        raise HTTPException(status_code=404, detail="Task Group not found")
    return {
        "name": task_group.name,
        "tasks": task_group.tasks
    }


@app.get("/winrmtask/wmi/results")
async def get_wmi(projection: Annotated[str | None, Header()] = None):
    async with MongoDBHandler() as handler:
        print(f"PROJECTION: {projection}")
        return [i async for i in handler.find(collection='wmi_hosts', projection={'_id': 0} | json.loads(projection))]


@app.get("/winrmtask/{name}/results")
async def get_task_group_results(name: str):
    if name == 'all':
        async with MongoDBHandler() as handler:
            return [i async for i in handler.find(collection='winrm_hosts', projection={'_id': 0})]
    async with MongoDBHandler() as handler:
        return [i async for i in handler.find(collection='winrm_hosts', projection={name: 1})]


@app.get("/winrmtask/{name}/results/{host}")
async def get_task_group_results_for_host(name: str, host: str):
    async with MongoDBHandler() as handler:
        return tf.json_to_dict(await handler.find(collection='winrm_hosts',
                                                  selection={'hostname': host},
                                                  projection={name: 1}))

@app.post("/winrmtask/{name}")
async def run_task(name: str):
    task = await WinRMTaskGroup.fetch_task(name)
    await task.execute()

@app.post("/winrmtask/{name}/{group}")
async def run_task_in_hostgroup(name: str, group: str):
    task = await WinRMTaskGroup.fetch_task(name)
    group = await HostGroup.fetch_hostgroup(group)
    await task.execute(group=group)

@app.put("/winrmtask")
async def create_task(name: Annotated[str, Header()], 
                      tasks: Annotated[list(WinRMTask), Header()],
                      host_groups: Annotated[list(HostGroup), Header()]):
    winrm_tasks = []
    for i in tasks:
        winrm_tasks.append({j.name: WinRMConnection.encode_command(j.script) for j in i})
    await WinRMTaskGroup.create_task(host_groups=host_groups, tasks=winrm_tasks, name=name)

@app.post("/winrmtask/update")
async def update_task(name: Annotated[str, Header()],
                      tasks: Annotated[list(WinRMTask), Header()],
                      host_groups: Annotated[list(HostGroup), Header()]):
    async with MongoDBHandler() as handler:
        if not tasks:
            await handler.upsert_one('winrm_task_groups', 
                                    selection={"name": name},
                                    operator="$set",
                                    data={"host_groups": host_groups})
            return
        winrm_tasks = []
        for i in tasks:
            winrm_tasks.append({j.name: WinRMConnection.encode_command(j.script) for j in i})
        await handler.upsert_one('winrm_task_group',
                                 selection={"name": name},
                                 operator="$set",
                                 data={"tasks": winrm_tasks})

################################################################################################
################################################################################################
########################################### GROUPS #############################################
################################################################################################
################################################################################################


@app.get("/winrmhosts")
async def fetch_all_host_groups():
    async with MongoDBHandler() as handler:
        host_groups = [i async for i in handler.find(collection='winrm_host_groups', projection={'_id': 0})]
        return host_groups


@app.get("/winrmhosts/{name}")
async def fetch_host_group(name: str):
    host_group = await HostGroup.fetch_hostgroup(name)
    hosts = [i async for i in host_group]
    if host_group.size == 0:
        raise HTTPException(status_code=404, detail="Host Group not found")
    return {
        "name": host_group.name,
        "description": host_group.description,
        "hosts": hosts
    }
