import pymongo
from pymongo import InsertOne, MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import json
import os
import toml

class DBHandler:
    __server : str
    __port : int
    __user : str
    __password : str
    __connection : MongoClient
    is_connected : bool = False
    
    
    def __parse_user(self, user: str) -> str:
        for i in ['^', '~', '´', '`', '=', '+', '*', '?', '/', '{', '}', '[', ']', '(', ')', '%', '$', '#', '@', '!', '&', '¨', "'", '"']:
            if i in user:
                raise TypeError("Formatting of user name is invalid")
        return user

    def __parse_port(self, port : int) -> int:
        if port not in range(65535):
            raise TypeError("Invalid port number for server")
        return port
    
    def __fetch_configuration(self):
        try:
            absolute = os.path.dirname(__file__)
            relative = os.path.join(absolute, '../../resources/config.toml')
            with open(relative, 'r') as config_file:
                toml_file = toml.loads(config_file.read())
                if 'ldap' in toml_file.keys():
                    self.__server = toml_file['mongodb']['server']
                    
                    self.__port = 27017
                    
                    self.__user = self.__parse_user(toml_file['mongodb']['user'])
                    self.__password = toml_file['mongodb']['password']
                else:
                    print('Configuration file doesn\'t have information regarding the LDAP connection')
        except FileNotFoundError:
            print('Configuration file not found in path, the default path for this is /etc/verdete/config.toml')
    def __init__(self):
        self.__fetch_configuration()
    
    def connect(self, collection: str):
        if not collection:
            raise ValueError("Collection must not be null")
        else:
            self.__connection = MongoClient(f"mongodb://{self.__user}:{self.__password}@{self.__server}:{self.__port}")
            database = self.__connection.verdete
            collection = database.get_collection(collection)
            self.is_connected = True
            return collection
    
    def insert(self, collection, value : dict):
        collection = self.__connection.verdete.get_collection(collection)
        collection.insert_one(value)
    
    def upsert(self, collection, value: dict):
        collection = self.__connection.verdete.get_collection(collection)
        collection.update_one({"Hostname": value["Hostname"]}, {"$set": {value["Task Name"]: value}}, upsert=True)
    
    def close(self):
        self.__connection.close()