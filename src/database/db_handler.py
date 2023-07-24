from src.util.task_formatter import TaskFormatter as tf
from pymongo import MongoClient
from typing import Optional, Literal
from collections import namedtuple
import websockets
import os
import toml

Index = namedtuple('Index', ['name', 'columns'])
Field = namedtuple('Field', ['name', 'type', 'value'])


class MongoDBHandler:
    __url: str
    is_connected: bool
    mongo_client: MongoClient

    def __init__(self):
        self.__fetch_configuration()

    async def __aenter__(self):
        self.mongo_client = MongoClient(host=self.url)
        return self

    def __fetch_configuration(self):
        try:
            path = os.path.join(os.path.dirname(__file__),
                                '../../resources/config.toml')
            with toml.loads(open(path, 'r').read()) as toml_file:
                if 'surrealdb' in toml_file.keys():
                    user = toml_file["mongodb"]["user"]
                    password = toml_file["mongodb"]["user"]
                    server = toml_file["mongodb"]["server"]
                    port = toml_file["mongodb"]["port"] if not None else 27017

                    self.url = f"mongodb://{user}:{password}@{server}:{port}/verdete"
                else:
                    print('Configuration file doesn\'t have information regarding the SurrealDB connection')
        except FileNotFoundError:
            print('Configuration file not found in path, the default path for this is /etc/verdete/config.toml')

    async def insert(self, collection: str, data: list,
                     mode: Literal["csv", "json", "xml", "ps_table", "dict", "single_value"] = "single_value"):
        pass

    async def upsert(self, collection: str, data: list,
                     mode: Literal["csv", "json", "xml", "ps_table", "dict", "single_value"] = "single_value"):
        pass

    async def update(self, collection: str, data: list,
                     mode: Literal["csv", "json", "xml", "ps_table", "dict", "single_value"] = "single_value"):
        pass
