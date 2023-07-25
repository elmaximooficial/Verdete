from src.util.task_formatter import TaskFormatter as tf
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Literal
from collections import namedtuple
import os
import toml
import json

Index = namedtuple('Index', ['name', 'columns'])
Field = namedtuple('Field', ['name', 'type', 'value'])


class MongoDBHandler:
    user: str
    password: str
    server: str
    port: int
    is_connected: bool
    mongo_client: AsyncIOMotorClient

    def __init__(self):
        self.__fetch_configuration()

    async def __aenter__(self):
        self.mongo_client = AsyncIOMotorClient(f'mongodb://{self.user}:{self.password}@{self.server}:{self.port}', connect=True)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def __fetch_configuration(self):
        try:
            path = os.path.join(os.path.dirname(__file__),
                                '../../resources/config.toml')
            with open(path, 'r') as config_file:
                toml_file = toml.loads(config_file.read())
                if 'mongodb' in toml_file.keys():
                    self.user = toml_file["mongodb"]["user"]
                    self.password = toml_file["mongodb"]["password"]
                    self.server = toml_file["mongodb"]["server"]
                    self.port = toml_file["mongodb"]["port"] if not None else 27017
                else:
                    print('Configuration file doesn\'t have information regarding the SurrealDB connection')
        except FileNotFoundError:
            print('Configuration file not found in path, the default path for this is /etc/verdete/config.toml')

    async def find(self, collection: str, selection: dict, projection: dict = None):
        async for i in self.mongo_client.get_database("verdete").get_collection(collection).find(filter=selection,
                                                                                                 projection=projection):
            yield i

    async def find_one(self, collection: str, selection: dict, projection: dict = None):
        return await self.mongo_client.get_database("verdete").get_collection(collection).find_one(filter=selection,
                                                                                                   projection=projection)

    async def insert(self, collection: str, data: list,
                     mode: Literal["csv", "json", "xml", "ps_table", "dict", "single_value"] = "single_value"):
        [await self.mongo_client.get_database("verdete").get_collection(collection).insert_one(record) for record in data]

    async def upsert(self, collection: str, data: list,
                     mode: Literal["csv", "json", "xml", "ps_table", "dict", "single_value"] = "single_value"):
        pass

    async def update(self, collection: str, data: list,
                     mode: Literal["csv", "json", "xml", "ps_table", "dict", "single_value"] = "single_value"):
        pass
