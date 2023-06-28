from queue import Queue
from src.winrm.host import Host
from src.winrm.host_group import HostGroup
from src.util.password_manager import User
from src.util.ldap import LDAP
from src.winrm.windows import *

class TaskGroup:
    tasks : list
    transport : WINRM_TRANSPORT
    
    def __init__(self, *args, transport):
        self.tasks = []
        self.transport = transport
        self.tasks.extend(iter(args))
    
    async def execute(self, host : Host, user : User, group : HostGroup = None):
        print(host.hostname)
        success, conn, shell_id = await create_connection(host, user, self.transport)
        if not success:
            yield {"Hostname": host.hostname, "Status": "Failure", "Error": shell_id}
        else:
            raw_dict = {host.hostname: {}}
            for i in self.tasks:
                command_id, stdout, stderr, status = await execute_command(host, user, i.script, self.transport, conn, shell_id)
                conn.cleanup_command(shell_id, command_id)
                if status == 0 and len(stdout) >= 5:
                    raw_dict[host.hostname][i.name] = {}
                    for line in stdout.replace('\r', '').split('\n'):
                        if line.strip():
                            name, value = line.split('\t')
                            raw_dict[host.hostname][i.name][name] = value
                else:
                    raw_dict[host.hostname][i.name]["Hostname"] = host.hostname
                    raw_dict[host.hostname][i.name]["Error Message"] = stderr
            conn.close_shell(shell_id)
            yield raw_dict