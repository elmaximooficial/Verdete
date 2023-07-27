import asyncio
import functools

from src.database.db_handler import MongoDBHandler
from src.winrm.host_group import HostGroup
from src.winrm.task_group import WinRMTaskGroup
from src.util.task_formatter import TaskFormatter as tf
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

@app.post("/winrmtask/{name}/run/{group}")
async def run_task(name: str, group: str):
    task = await WinRMTaskGroup.fetch_task(name)
    group = await HostGroup.fetch_hostgroup(group)
    async with asyncio.TaskGroup() as tg:
        tg.create_task(task.execute(group=group))

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
