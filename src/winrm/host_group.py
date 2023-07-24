import concurrent.futures
from asyncio import Queue
from src.winrm.windows import WinRMConnection, WINRM_TRANSPORT, WINRM_PROTOCOL
from src.util.password_manager import User
from collections import namedtuple
import asyncio
import threading


Host = namedtuple(typename="Host",
                  field_names=["hostname", "port", "protocol", "transport"],
                  defaults=[5985, WINRM_PROTOCOL.HTTP, WINRM_TRANSPORT.NTLM])


class HostGroup:
    hosts: list
    name: str
    description: str
    __index: int
    connections: Queue
    user: User
    
    def __init__(self, *host, name: str, description: str, user: User):
        self.name = name
        self.description = description
        self.hosts = list(host)
        self.connections = Queue()
        self.user = user
        self.__index = 0

    def add_host(self, host: Host):
        self.hosts.append(host)

    async def __aenter__(self):
        async with asyncio.TaskGroup() as tg:
            for i in self.hosts:
                conn = WinRMConnection(endpoint=f"{i.protocol}://{i.hostname}:{i.port}/wsman",
                                       transport=i.transport,
                                       username=self.user.username,
                                       password=self.user.password,
                                       server_cert_validation='ignore',
                                       operation_timeout_sec=15,
                                       read_timeout_sec=30)
                tg.create_task(conn.connect())
                await self.connections.put(conn)
                print(f"Connected to {conn.transport.endpoint}")
        return self

    async def get(self):
        return await self.connections.get()

    async def put(self, connection: WinRMConnection):
        await self.connections.put(connection)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.connections.empty():
            while True:
                conn = await self.connections.get()
                if conn is None:
                    break
