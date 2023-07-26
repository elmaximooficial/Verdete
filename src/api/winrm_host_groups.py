from fastapi_app import app
from src.winrm.host_group import HostGroup
from src.database.db_handler import MongoDBHandler


@app.get("/winrmhosts/")
async def fetch_all_host_groups():
    async with MongoDBHandler() as handler:
        host_groups = [i for i in await handler.find('winrm_host_groups')]


@app.get("/winrmhosts/{name}")
async def fetch_host_group(name: str):
    host_group = await HostGroup.fetch_hostgroup(name)
    return {
        "name": host_group.name,
        "description": host_group.description,
        "hosts": host_group.__hosts
    }
