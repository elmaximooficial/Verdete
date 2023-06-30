import asyncio
import sys, getopt
from src.winrm.windows import WINRM_TRANSPORT
from src.util.ldap import LDAP
from src.winrm.task import Task, FAILURE_ACTION
from src.winrm.task_group import TaskGroup
from src.winrm.host import Host
from src.util.password_manager import PasswordManager, User
from src.winrm.host_group import HostGroup
from getpass import getpass
import json

########## Configuration file format ##########
#### [ldap]                              
#### server = address_to_server
#### port = port_for_server (optional, default=389)
#### base_dn = root dn for searching computers
#### use_ssl = Allow for ssl
#### user = User for connection to the database
#### domain = User domain name



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
                
                
                cpu_task = Task("CPU", r'powershell -c " $_ = Get-WmiObject Win32_Processor; Invoke-Command {"""Name`t$($_.Name)`nCaption`t$($_.Caption)`nNumber of Cores`t$($_.NumberOfCores)`nNumber of Logical Processors`t$($_.NumberOfLogicalProcessors)"""}"', FAILURE_ACTION.STOP_EXECUTION, WINRM_TRANSPORT.NTLM)
                os_task = Task("OS", r'powershell -c "$_ = Get-WmiObject Win32_OperatingSystem; Invoke-Command {"""Caption`t$($_.Caption)`nBuild Number`t$($_.BuildNumber)`nOS Architecture`t$($_.OSArchitecture)`nDescription`t$($_.Description)"""}"', FAILURE_ACTION.STOP_EXECUTION, WINRM_TRANSPORT.NTLM)
                net_task = Task("Networking", r'powershell -c "$_ = Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $True}; Invoke-Command {"""IP Address`t$($_.IPAddress[0])`nDefault Gateway`t$($_.DefaultIPGateway[0])`nDescription`t$($_.Description)`nIndex`t$($_.Index)`nDHCP Enabled`t$($_.DHCPEnabled)"""}"', FAILURE_ACTION.STOP_EXECUTION, WINRM_TRANSPORT.NTLM)
                
                task_group = TaskGroup(cpu_task, os_task, net_task, transport=WINRM_TRANSPORT.NTLM)
                
                computers = ['PM-CPDADM001', 'PM-CPDADM002', 'PM-CPDADM003', 'PM-CPDADM004', 'PM-SAFCPD007', 'ADM002', 'PM-NOTEINFO99']
                
                host_group = HostGroup("CPD", Host("PM-CPDADM001"), Host("PM-CPDADM002"), Host("PM-CPDADM004"), Host("PM-SADCPD007"), Host("ADM002"), Host("PM-NOTEINFO99"))
                
                async for i in task_group.execute(group=host_group, user=user):
                    print(i)
                
                async for i in ldap_conn.fetch_computers():
                    async for i in task_group.execute(Host(i), user):
                        print(i)

if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main(sys.argv[1:]))