class HostGroup:
    hosts: list
    name: str
    description: str
    __index: int
    
    def __init__(self, *host, name : str, description : str):
        self.name = name
        self.description = description
        self.hosts = list(host)
        self.__index = 0

    def __aiter__(self):
        return self
    async def __anext__(self):
        if self.__index >= len(self.hosts):
            raise StopAsyncIteration
        item = self.hosts[self.__index]
        self.__index += 1
        return item
    def __getitem__(self, idx : int):
        return self.hosts[idx]
