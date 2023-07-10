from queue import Queue
from src.winrm.host import Host
from src.winrm.host_group import HostGroup
from src.util.password_manager import User
from src.util.ldap import LDAP
from src.winrm.windows import *
from src.database.db_handler import DBHandler
import json

class TaskGroup:
    tasks : list
    transport : WINRM_TRANSPORT
    current_task : str
    
    def __init__(self, *args, transport):
        self.tasks = []
        self.transport = transport
        self.tasks.extend(iter(args)) 
    
    def _format_results(self, task_name : str, hostname : str, result : list):
        raw_dict = {"Hostname": hostname, "Status" : "Success", "Results" : {}}
        raw_dict["Results"][task_name] = {}
        for line in result:
            if line.strip():
                name, value = line.split('\t')
                raw_dict["Results"][task_name][name] = value
        return raw_dict
        
    def _format_error(self, task_name : str, hostname : str, error_message : str):
        return {"Hostname": hostname, "Status": "Failure", "Results": {task_name: {"Error Message": error_message}}}
    
    async def _execute_task(self, user : User, host):
        success, conn, shell_id = await create_connection(host, user, self.transport)
        if not success:
            yield json.dumps({"Hostname": host.hostname, "Status": "Failure", "Error": shell_id}, indent=4)
        else:
            for i in self.tasks:
                self.current_task = i.name
                command_id, stdout, stderr, status = await execute_command(host, user, i.stages["Stages"][1], self.transport, conn, shell_id)
                conn.cleanup_command(shell_id, command_id)
                if status != 0 or len(stdout) < 5:
                    yield json.dumps(self._format_error(i.name, host.hostname, stderr))
                else:
                    yield json.dumps(self._format_results(i.name, host.hostname, stdout.replace('\r', '').split('\n')), indent=4)
            conn.close_shell(shell_id)
    
    async def __insert_into_db(self, value : str, handler : DBHandler, collection):
        if handler.is_connected:
            print(json.loads(value))
            handler.insert(collection, json.loads(value))
        else:
            raise RuntimeError("Database is not connected")
    
    async def execute(self, user : User, group : HostGroup = None, host : Host = None, debug : bool = False, db_handler : DBHandler = None, collection = None):
        """Executes the Task group on the determined host or host group, returns a string formatted in json with 4 space indentation

        Args:
            host (Host): The host this Task group should be executed on
            user (User): The User for authenticating the connection on the remote WinRM port
            group (HostGroup, optional): The Host Group this Task Group should be executed on. Defaults to None.

        Yields:
            str: The JSON string containing the returned values
        """
        if host:
            async for i in self._execute_task(user, host):
                if debug:
                    yield i
                else:
                    await self.__insert_into_db(i, db_handler, collection)
        if group:
            for i in group:
                async for j in self._execute_task(user, i):
                    if debug:
                        yield j
                    else:
                        await self.__insert_into_db(j, db_handler, collection)