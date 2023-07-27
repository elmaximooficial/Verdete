from src.api.fastapi_app import app
from src.winrm.host_group import HostGroup
from src.database.db_handler import MongoDBHandler
from fastapi import HTTPException

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
