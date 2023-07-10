import asyncio
import sys, getopt
from src.winrm.windows import WINRM_TRANSPORT
from src.util.ldap import LDAP
from src.winrm.task import Task, FAILURE_ACTION
from src.winrm.task_group import TaskGroup
from src.winrm.host import Host
from src.util.password_manager import PasswordManager, User
from src.winrm.host_group import HostGroup
from src.database.db_handler import DBHandler
from getpass import getpass
import json
import aiofiles

########## Configuration file format ##########
#### [ldap]                              
#### server = address_to_server
#### port = port_for_server (optional, default=389)
#### base_dn = root dn for searching computers
#### use_ssl = Allow for ssl
#### user = User for connection to the database
#### domain = User domain name
#### [mongodb]
#### server = address_to_server
#### port = server_port
#### user = server's user
#### password = password
#### database = database

def hostname_check(result : dict):
    print(result["Results"]["OS"]["Hostname"])
    return result["Results"]["OS"]["Hostname"] == "PM-NOTEINFO99"

class Main:
    async def main(self, argv):
        opts, args = getopt.getopt(argv, '', ['fetch-computers', 'gen-password=', 'gen-key', 'query-computers'])
        for i, arg in opts:
            if i in ['--gen-password']:
                pass_manager = PasswordManager.load_key()
                username, password = arg.split('~')
                pass_manager.gen_encrypted_pwd(username=username, password=password)
            if i in ['--gen-key']:
                PasswordManager.gen_key()
            if i in ['--fetch-computers']:
                ldap_conn = LDAP()
                await ldap_conn.connect_to_server()
                async for i in ldap_conn.fetch_computers():
                    print(i)
                await ldap_conn.dispose_connection()
            if i in ['--query-computers']:
                ldap_conn = LDAP()
                await ldap_conn.connect_to_server()
                
                username = input('Insert the Username: ')
                password = getpass('Insert the Password: ')
                
                user = User(username, password)
                
                wmi_check = lambda x: x != None
                cpu_task = Task(name="CPU", 
                #            pre_check=r'powershell -c " """Hostname`t$(hostname)""" "', 
                #            pre_checking=wmi_check, 
                #            pre_check_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                            script=r'powershell -c " $_ = Get-WmiObject Win32_Processor; Invoke-Command {"""Name`t$($_.Name)`nCaption`t$($_.Caption)`nNumber of Cores`t$($_.NumberOfCores)`nNumber of Logical Processors`t$($_.NumberOfLogicalProcessors)"""}"', 
                            script_checking=wmi_check, 
                            script_failure_action=FAILURE_ACTION.STOP_EXECUTION, 
                            transport=WINRM_TRANSPORT.NTLM)
                os_task = Task(name="OS", 
                #            pre_check=r'powershell -c " """Hostname`t$($hostname)""" "', 
                #            pre_checking=hostname_check, 
                #            pre_check_failure_action=FAILURE_ACTION.ALTERNATIVE_TASK, 
                #            pre_check_alternative=cpu_task, 
                            script=r'powershell -c "$_ = Get-WmiObject Win32_OperatingSystem; Invoke-Command {"""Caption`t$($_.Caption)`nBuild Number`t$($_.BuildNumber)`nOS Architecture`t$($_.OSArchitecture)`nDescription`t$($_.Description)"""}"', 
                            script_checking=wmi_check,
                            script_failure_action=FAILURE_ACTION.STOP_EXECUTION, 
                            transport=WINRM_TRANSPORT.NTLM)
                net_task = Task(name="Networking", 
                            script=r'powershell -c "$_ = Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $True}; Invoke-Command {"""IP Address`t$($_.IPAddress[0])`nDefault Gateway`t$($_.DefaultIPGateway[0])`nDescription`t$($_.Description)`nIndex`t$($_.Index)`nDHCP Enabled`t$($_.DHCPEnabled)"""}"', 
                            script_checking=wmi_check,
                            script_failure_action=FAILURE_ACTION.STOP_EXECUTION, 
                            transport=WINRM_TRANSPORT.NTLM)
                
                task_group = TaskGroup(cpu_task, os_task, net_task, transport=WINRM_TRANSPORT.NTLM)
                
                computers = ['PM-CPDADM001', 'PM-CPDADM002', 'PM-CPDADM003', 'PM-CPDADM004', 'PM-SAFCPD007', 'ADM002', 'PM-NOTEINFO99']
                
                host_group = HostGroup(Host("PM-CPDADM001"), Host("PM-CPDADM002"), Host("PM-CPDADM004"), Host("PM-SAFCPD007"), Host("ADM002"), Host("PM-NOTEINFO99"), name="CPD", description="Computers from ITD")
                
                
                available = HostGroup(name="Available", description="All Computers Available")
                #for i in computers:
                #    async for j in os_task.execute(Host(i), user):
                #        print(j)
                
                #async for i in task_group.execute(group=host_group, user=user):
                #    print(i)
                #    if json.loads(i)["Status"] == "Success":
                #        available.hosts.append(Host(json.loads(i)["Hostname"])
                    
                db_handler = DBHandler()
                collection = db_handler.connect(collection='hosts')
                async for i in ldap_conn.fetch_computers():
                    async for i in task_group.execute(host=Host(i), user=user, db_handler=db_handler, collection=collection):
                        print(i)
if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main(sys.argv[1:]))