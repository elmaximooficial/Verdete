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
    """
    A helper class for handling Database queries, use this in Async Context Manager.
    The configurations for this class are loaded from the config.toml file
    """
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

    async def find(self, collection: str, selection: dict = None, projection: dict = None):
        """
        This is an async generator object
        :param collection: The collection in which to query
        :param selection: The filter of the query, this is a dictionary in standard MongoDB format
        :param projection: The field selection of the query, this is a dictionary in standard MongoDB format

        :return: Each document present in the Cursor
        """
        async for i in self.mongo_client.get_database("verdete").get_collection(collection).find(filter=selection,
                                                                                                 projection=projection):
            yield i

    async def find_one(self, collection: str, selection: dict = None, projection: dict = None):
        """
        Queries the database for one document and returns it directly
        :param collection: The collection in which to search for the document
        :param selection: The filter of the query, this is a dictionary in standard MongoDB format
        :param projection: The field selection of the query, this is a dictionary in standard MongoDB format

        :return: The document present in the cursor
        """
        return await self.mongo_client.get_database("verdete").get_collection(collection).find_one(filter=selection,
                                                                                                   projection=projection)

    async def insert(self, collection: str, data: dict):
        """
        Inserts the 'data' dictionary, should only be used for few inserts, in case of massive
        batch inserts, use insert_batch instead
        :param collection: The collection in which to insert the documents
        :param data: The dictionary to be inserted into the database

        :return: The status of the insertion
        """
        result = await self.mongo_client.get_database("verdete").get_collection(collection).insert_one(data)
        return {"Acknowledged": result.acknowledged, "ID": result.inserted_id}

    async def insert_batch(self, collection: str, data: list):
        """
        Inserts a batch of documents into 'collection'
        :param collection: The collection in which to insert documents
        :param data: A list of the documents to be inserted
        :return: The results of the operation in low-level detail
        """
        result = await self.mongo_client.get_database("verdete").get_collection(collection).bulk_write(data)
        return result.bulk_api_result

    async def repsert_one(self, collection: str, selection: dict, data: dict):
        """
        Replaces the collection's document matched in the selection with the 'data' dictionary
        :param collection: The collection in which to search the document
        :param selection: The filter for the query, this is a dictionary in MongoDB format
        :param data: The document to replace the match, this is a dictionary in MongoDB format
        :return: The results of the query
        """
        result = await self.mongo_client.get_database("verdete").get_collection(collection).replace_one(filter=selection,
                                                                                                        update=data,
                                                                                                        upsert=True)

        return {
            "Acknowledged": result.acknowledged,
            "Matched Count": result.matched_count,
            "Modified Count": result.modified_count,
            "Raw Result": result.raw_result,
            "Upserted ID": result.upserted_id
        }

    async def upsert_one(self, collection: str, selection: dict, operator: str, data: dict):
        """
        Updates the matched document with the 'data' using the 'operator', this is a 'one' upsert, for batch updates
        use upsert_many instead
        :param collection: The collection in which to search the document
        :param selection: The filter for the query, this is a dictionary in MongoDB format
        :param operator: The operator to be executed in the match for the data
        :param data: The attributes to be operated with
        :return: The results of the query
        """
        result = await self.mongo_client.get_database("verdete").get_collection(collection).update_one(filter=selection,
                                                                                                       update={operator: data},
                                                                                                       upsert=True)
        return {
            "Acknowledged": result.acknowledged,
            "Matched Count": result.matched_count,
            "Modified Count": result.modified_count,
            "Raw Result": result.raw_result,
            "Upserted ID": result.upserted_id
        }

    async def upsert_many(self, collection: str, selection: dict, operator: str, data: list):
        """
        Updates the matched document with the 'data' using the 'operator'
        :param collection: The collection in which to search the document
        :param selection: The filter for the query, this is a dictionary in MongoDB format
        :param operator: The operator to be executed in the match for the data
        :param data: The attributes to be operated with
        :return: The results of the query
        """
        result = await self.mongo_client.get_database("verdete").get_collection(collection).update_many(filter=selection,
                                                                                                        update={operator: data},
                                                                                                        upsert=True)
        return
        {
            "Acknowledged": result.acknowledged,
            "Matched Count": result.matched_count,
            "Modified Count": result.modified_count,
            "Raw Result": result.raw_result,
            "Upserted ID": result.upserted_id
        }