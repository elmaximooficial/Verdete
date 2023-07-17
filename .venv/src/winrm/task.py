from __future__ import annotations
from src.util.password_manager import User
from src.winrm.windows import *
from src.winrm.host import Host
from enum import StrEnum, IntEnum
from winrm.exceptions import *
from requests.exceptions import *
from typing import Callable
import json

class FAILURE_ACTION(StrEnum):
    STOP_EXECUTION = 'stop_execution'
    RESTART_EXECUTION = 'restart_execution'
    ALTERNATIVE_TASK = 'alternative_task'

class STAGES(IntEnum):
    PRE_CHECK = 0
    SCRIPT = 1
    POST_CHECK = 2

class Task:
    name : str
    
    stages : dict
    
    transport : WINRM_TRANSPORT
    pre_check : Callable
    script_check : Callable
    post_check : Callable
    
    max_iterations : int
    
    def __init__(self,
                name : str,
                script : str,
                script_failure_action : FAILURE_ACTION,
                script_checking : Callable,
                transport : WINRM_TRANSPORT,
                pre_check : str = None, 
                pre_checking : Callable = None,
                post_check : str = None,
                post_checking : Callable = None,
                pre_check_failure_action : FAILURE_ACTION = None,
                post_check_failure_action : FAILURE_ACTION = None,
                pre_check_alternative : Task = None,
                script_alternative : Task = None,
                post_check_alternative : Task = None,
                max_iterations : int = 5
                ):
        self.name = name
        self.stages = {
            "Stages": [
                pre_check, 
                script, 
                post_check
            ],
            "Failure Actions": [
                pre_check_failure_action, 
                script_failure_action,
                post_check_failure_action
            ],
            "Alternative Tasks": [
                (pre_check_alternative or None),
                (script_alternative or None),
                (post_check_alternative or None)
            ],
            "Iterations": [0,0,0]
        }
        self.transport = transport
        self.max_iterations = max_iterations
        self.pre_check = pre_checking
        self.script_check = script_checking
        self.post_check = post_checking
    
    def __check_stage(self,
                    index : int,
                    out : dict):
        if index == 0:
            return self.pre_check(out)
        elif index == 1:
            return self.script_check(out)
        elif index == 2:
            return self.post_check(out)
        else:
            raise TypeError("Invalid stage index")
    
    def _format_error(self,
                    hostname : str,
                    stage : str, 
                    error_message : str):
        return {"Hostname": hostname, "Status": f"{stage} Error", "Error Message": error_message}
        
    def _format_results(self,
                    hostname : str,
                    results : str,
                    stage : str):
        results = results.split("\n")
        raw_dict = {"Hostname": hostname, "Status" : f"{stage} Success", "Results" : {}}
        raw_dict["Results"][self.name] = {}
        for line in results:
            if line.strip():
                name, value = line.split('\t')
                raw_dict["Results"][self.name][name] = value
        return raw_dict
    
    async def __execution_switch(self,
                        index : int,
                        host : Host,
                        user : User,
                        conn : Protocol,
                        shell_id : str,
                        err : str):
        if self.stages["Failure Actions"][index] == FAILURE_ACTION.RESTART_EXECUTION and self.stages["Iterations"][index] < self.max_iterations:
            self.stages["Iterations"][index] += 1
            async for i in self.__execute_stage(index, host, user, conn, shell_id):
                yield i
        elif self.stages["Failure Actions"][index] == FAILURE_ACTION.STOP_EXECUTION or self.stages["Iterations"][index] == self.max_iterations:
            yield json.dumps(self._format_error(host.hostname, STAGES(index), err), indent=2)
        elif self.stages["Failure Actions"][index] == FAILURE_ACTION.ALTERNATIVE_TASK:
            print(json.dumps(self._format_error(host.hostname, STAGES(index), err), indent=2))
            async for i in self.stages["Alternative Tasks"][index].execute(host, user):
                yield i
    
    async def __execute_stage(self,
                            index : int,
                            host : Host,
                            user : User,
                            conn : Protocol,
                            shell_id : str):
        command_id, out, err, status = await execute_command(host, user, self.stages["Stages"][index], self.transport, conn, shell_id)
        if status != 0 or len(out) <= 5 or self.__check_stage(index, self._format_results(host.hostname, out.replace("\r", ""), STAGES(index))) != True:
            if not err:
                err = f"Check for stage {index} Failed"
            async for i in self.__execution_switch(index, host, user, conn, shell_id, err):
                yield (command_id, i)
        else:
            yield (command_id, json.dumps(self._format_results(host.hostname, out.replace("\r", ""), STAGES(index)), indent=2))

    async def execute(self, 
                host : Host, 
                user : User,
                is_task_group : bool = False) -> str:

        if not is_task_group:
            success, conn, shell_id = await create_connection(host, user, self.transport)
            if success:
                command_id = None
                for i in range(len(self.stages["Stages"])):
                    if self.stages["Stages"][i]:
                        async for cid,j in self.__execute_stage(i, host, user, conn, shell_id):
                            if json.loads(j)["Status"] == f"{i} Error":
                                yield j
                                return
                            command_id = cid
                            yield j
                await dispose_shell(shell_id, command_id, conn)
            else:
                yield self._format_error(host.hostname, "Connection", shell_id)