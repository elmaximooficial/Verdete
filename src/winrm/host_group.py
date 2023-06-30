class HostGroup:
    hosts : list
    name : str
    description : str
    __index : int
    
    def __init__(self, *host, name : str, description : str):
        self.name = name
        self.description = description
        self.hosts = list(host)
    def __next__(self):
        if self.__index >= len(self.hosts):
            raise StopIteration
        item = self.hosts[self.__index]
        self.__index += 1
        return item
    def __getitem__(self, idx : int):
        return self.hosts[idx]
