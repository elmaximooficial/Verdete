from __future__ import annotations
from src.util.password_manager import User
from src.winrm.windows import execute_command, WINRM_TRANSPORT
from src.winrm.host import Host
from enum import StrEnum
from winrm.exceptions import *
from requests.exceptions import *

class FAILURE_ACTION(StrEnum):
    STOP_EXECUTION = 'stop_execution'
    RESTART_EXECUTION = 'restart_execution'
    ALTERNATIVE_TASK = 'alternative_task'

class Task:
    name : str
    pre_check : str
    pre_check_expect : any
    script : str
    script_expect : any
    post_check : str
    post_check_expect : any
    pre_check_failure_action : FAILURE_ACTION
    script_failure_action : FAILURE_ACTION
    post_check_failure_action : FAILURE_ACTION
    pre_check_alternative : Task
    script_alternative : Task
    post_check_alternative : Task
    transport : WINRM_TRANSPORT
    
    def __init__(self,
                name : str,
                script : str,
                script_failure_action : FAILURE_ACTION,
                transport : WINRM_TRANSPORT,
                pre_check : str = None, 
                pre_check_expect : any = None,
                script_expect : any = None,
                post_check : str = None,
                post_check_expect : any = None,
                pre_check_failure_action : FAILURE_ACTION = None,
                post_check_failure_action : FAILURE_ACTION = None,
                pre_check_alternative : Task = None,
                script_alternative : Task = None,
                post_check_alternative : Task = None
                ):
        """ Creates a new instance of a Task, use this class for executing pre-baked scripts in either Powershell or CMD syntax.

        Args:
            pre_check (str): A conditional statement for checking the state of the machine before the script is executed.     
            script (str): The actual commands to be executed on the host.
            post_check (str): A conditional statement for checking the state of the machine after the script is executed.
        """
        self.name = name
        self.pre_check = pre_check
        self.pre_check_expect = pre_check_expect
        self.script = script
        self.script_expect = script_expect
        self.post_check = post_check
        self.post_check_expect = post_check_expect
        self.pre_check_failure_action = pre_check_failure_action
        self.script_failure_action = script_failure_action
        self.post_check_failure_action = post_check_failure_action
        self.pre_check_alternative = pre_check_alternative
        self.script_alternative = script_alternative
        self.post_check_alternative = post_check_alternative
        self.transport = transport
        
    async def execute(self, 
                host : Host, 
                user : User) -> str:
        """ Executes a task on the given host. This only works for single machines.

        Args:
            host (Host): The Host to be affected by this task
            user (User): User with enough privileges to run this task
            pre_check_failure_action (FAILURE_ACTION): What to do if the pre-check fails
            script_failure_action (FAILURE_ACTION): What to do if the script fails
            post_check_failure_action (FAILURE_ACTION): What to do if the post-check fails
            pre_check_alternative (Task, optional): If pre_check_failure_action is ALTERNATIVE_TASK, this task will be executed. Defaults to None
            script_alternative (Task, optional): If the script_failure_action is ALTERNATIVE_TASK, this task will be executed. Defaults to None
            post_check_alternative (Task, optional): If the post_check_failure_action is ALTERNATIVE_TASK, this task will be executed. Defaults to None.
        """
        try:
            while True:
                if self.pre_check:
                    pre_out, pre_err, pre_status = await execute_command(host.hostname, user, self.pre_check, self.transport)
                    if pre_status == 0 and pre_out == self.pre_check_expect:
                        out, err, status = await execute_command(host.hostname, user, self.script, self.transport)
                        if status == 0 and out == self.script_expect and self.post_check:
                            post_out, post_err, post_status = await execute_command(host.hostname, user, self.post_check, self.transport)
                            if post_status == 0 and post_out == self.post_check_expect:
                                return [(pre_out, pre_err, pre_status), (out, err, status), (post_out, post_err, post_status)]
                            else:
                                if self.post_check_failure_action == 'stop_execution':
                                    return (host.hostname, post_err)
                                elif self.post_check_failure_action == 'restart_execution':
                                    continue
                                elif self.post_check_failure_action == 'alternative_task':
                                    await self.post_check_alternative.execute(host, user)
                        else:
                            if self.script_failure_action == 'stop_execution':
                                return(host.hostname, post_err)
                            elif self.script_failure_action == 'restart_execution':
                                continue
                            elif self.script_failure_action == 'alternative_task':
                                await self.script_alternative.execute(host, user)
                    else:
                        if self.pre_check_failure_action == 'stop_execution':
                            return (host.hostname, pre_err)
                        elif self.pre_check_failure_action == 'restart_execution':
                            continue
                        elif self.pre_check_failure_action == 'alternative_task':
                            await self.pre_check_alternative.execute(host, user)
                else:
                    out, err, status = await execute_command(host.hostname, user, self.script, self.transport)
                    return (out, err, status)
        except ConnectionError:
            return (None, host.port, "No route to host")
        except InvalidCredentialsError:
            return (None, user.username, "Invalid Credentials")
        except ReadTimeout:
            return (None, user.username, "Read Timeout")
        
    def from_file(path : str, 
                delimiter : str,
                ) -> Task:
        with open(path, 'r') as file:
            pre_check, script, post_check, pre_action, action, post_action, pre_alt, script_alt, post_alt, transport = file.read().split(delimiter)
            task = Task(pre_check, script, post_check, pre_action, action, post_action, pre_alt, script_alt, post_alt, transport)
            return task