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

HostGroupQuery = namedtuple("HostGroupQuery", ['collection', 'selection'])

TempHostGroup = namedtuple("TempHostGroup", ['hostnames', 'user', 'size'])


class HostGroup:
    """
    This class is intended to represent a group o Windows hosts capable of communicating through WinRM, this host group
    will be stored in the database, and can be used as an argument to the TaskGroup.execute() method, which will iterate
    over the fetched hostnames in this host group.
    There are two static methods used for creating or loading a Host Group:
        :method fetch_hostgroup(name: str): Will load the Host Group with the name passed as argument from the database
        :method create_hostgroup(name: str, description: str, user: User, Optional(hosts: list), Optional(query: HostGroupQuery)):
        Will instantiate a new HostGroup object with the passed parameters, as well as insert it into the database
    The objects represented by this class will be stored in the winrm_host_groups collection.
    """
    __hosts: list
    __index: int
    name: str
    description: str
    user: User

    @staticmethod
    async def fetch_hostgroup(name: str):
        """
        Load the Host Group from the database, collection host_groups
        :param name: The name attribute of the document in host_groups collection

        :return: The constructed Host Group, loaded from the database
        """
        host_group = HostGroup(name=name)
        await host_group.__from_db()
        return host_group

    @staticmethod
    async def create_hostgroup(name: str,
                               description: str,
                               user: User,
                               hosts: list = None,
                               query: HostGroupQuery = None):
        """
        Creates a new Host Group and inserts it into the database
        :param name: The Host Group name, will be used to load the object later
        :param hosts: The List of Hosts associated with the Host Group, should be a list of Host()
        :param description: The description of the Host Group, should be used by the end-user for clarifying its purpose
        :param user: The username and password, certificate thumbprint, certificate path or token used for accessing the
        hosts in this host group
        :param query: There's an option to load the hostnames on-access, based on a Database query, this query will be
        stored in the __hosts variable, when loading the host group from the database, this query will be executed and
        the result stored in this object. Once loaded, this will not be executed again

        :return: Will return a Host Group object
        """
        host_group = HostGroup(name)
        if hosts is not None:
            host_group.__hosts = hosts
        elif query is not None:
            host_group.__hosts = query
        else:
            print("Either hosts or query should not be None, and exclusively one of them")
        host_group.description = description
        host_group.user = user
        await host_group.__create_new()

    def __init__(self, name: str):
        """
        Initializes the Host Group, attributing variables needed both for loading and saving the Host Group to the
        database
        :param name: The Host Group name
        """
        self.name = name
        self.__index = 0
        self.__hosts = []

    async def __from_db(self):
        """
        Loads the calling Host Group from the database
        """
        async with MongoDBHandler() as handler:
            database_host_group = await handler.find_one('winrm_host_groups', {"name": self.name})
            if not database_host_group:
                print(f"HostGroup {self.name} cannot be found on the database")
                return
            self.description = database_host_group['description']
            username = database_host_group['username']
            password = database_host_group['password']
            self.user = User(username, password)
            try:
                self.__hosts = [Host(i) for i in handler.find(database_host_group['hostnames']['collection'],
                                                              database_host_group['hostnames']['selection'],
                                                              {'hostnames': 1})]
            except:
                self.__hosts = database_host_group['hostnames']

    async def __create_new(self):
        """
        Inserts the object this function is called on in the database
        :return:
        """
        async with MongoDBHandler() as handler:
            await handler.insert("winrm_host_groups", {"name": self.name,
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

    @property
    def size(self):
        return len(self.__hosts)

