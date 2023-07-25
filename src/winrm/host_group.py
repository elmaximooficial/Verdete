import concurrent.futures
from asyncio import Queue
from src.database.db_handler import MongoDBHandler
from src.winrm.windows import WinRMConnection, WINRM_TRANSPORT, WINRM_PROTOCOL
from src.util.password_manager import User
from collections import namedtuple
import asyncio
import threading


Host = namedtuple(typename="Host",
                  field_names=["hostname", "port", "protocol", "transport"],
                  defaults=[5985, WINRM_PROTOCOL.HTTP, WINRM_TRANSPORT.NTLM])


class HostGroup:
    __hosts: list
    __index: int
    name: str
    description: str
    user: User

    @staticmethod
    async def fetch_hostgroup(hosts: list, name: str, description: str, user: User):
        host_group = HostGroup(name=name)
        await host_group.__from_db(hosts, name=name, description=description, user=user)
        return host_group

    def __init__(self, name: str):
        self.name = name
        self.__index = 0
        self.__hosts = []

    async def __from_db(self, hosts: list, name, description, user):
        async with MongoDBHandler() as handler:
            database_host_group = await handler.find_one('host_groups', {"name": self.name})
            if not database_host_group:
                await self.__create_new(hosts, name, description, user)
                return
            self.description = database_host_group['description']
            username = database_host_group['username']
            password = database_host_group['password']
            self.user = User(username, password)
            self.__hosts = database_host_group['hostnames']

    async def __create_new(self, hosts: list, name: str, description: str, user: User):
        self.__hosts.extend(hosts)
        self.name = name
        self.description = description,
        self.user = user
        async with MongoDBHandler() as handler:
            await handler.insert("host_groups", {"name": self.name,
                                                 "description": self.description,
                                                 "username": self.user.username,
                                                 "password": self.user.password,
                                                 "hostnames": [i._asdict() for i in self.__hosts]})

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.__index += 1
        if self.__index >= len(self.__hosts):
            raise StopAsyncIteration
        return self.__hosts[self.__index]

    def __getitem__(self, item):
        yield self.__hosts[item]

    def size(self):
        return len(self.__hosts)

