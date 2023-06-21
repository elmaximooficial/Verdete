from __future__ import annotations
from src.util.password_manager import User
from src.winrm.windows import WinRM
from enum import Enum

class FAILURE_ACTION(Enum):
    STOP_EXECUTION = 1
    RESTART_EXECUTION = 2
    ALTERNATIVE_TASK = 3

class Task:
    pre_check : str
    script : str
    post_check : str
    
    def __init__(self, pre_check : str, script : str, post_check : str):
        """ Creates a new instance of a Task, use this class for executing pre-baked scripts in either Powershell or CMD syntax.

        Args:
            pre_check (str): A conditional statement for checking the state of the machine before the script is executed.     
            script (str): The actual commands to be executed on the host.
            post_check (str): A conditional statement for checking the state of the machine after the script is executed.
        """
        self.pre_check = pre_check
        self.script = script
        self.post_check = post_check
    def execute(host : str, user : User, 
                pre_check_failure_action : FAILURE_ACTION, 
                script_failure_action : FAILURE_ACTION, 
                post_check_failure_action : FAILURE_ACTION,
                pre_check_alternative : Task = None,
                script_alternative : Task = None,
                post_check_alternative : Task = None):
        """ Executes a task on the given host. This only works for single machines.

        Args:
            host (str): The Hostname of the machine to be affected by this task
            user (User): User with enough privileges to run this task
            pre_check_failure_action (FAILURE_ACTION): What to do if the pre-check fails
            script_failure_action (FAILURE_ACTION): What to do if the script fails
            post_check_failure_action (FAILURE_ACTION): What to do if the post-check fails
            pre_check_alternative (Task, optional): If pre_check_failure_action is ALTERNATIVE_TASK, this task will be executed. Defaults to None
            script_alternative (Task, optional): If the script_failure_action is ALTERNATIVE_TASK, this task will be executed. Defaults to None
            post_check_alternative (Task, optional): If the post_check_failure_action is ALTERNATIVE_TASK, this task will be executed. Defaults to None.
        """
        