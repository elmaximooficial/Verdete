class HostGroup:
    hosts : list
    description : str
    __index : int
    
    def __init__(self, description : str, *host):
        self.description = description
        self.hosts = list(host)
    def __iter_(self):
        return self
    def __next__(self):
        if self.__index >= len(self.hosts):
            raise StopIteration
        item = self.hosts[self.__index]
        self.__index += 1
        return item
