import asyncio
import sys, getopt
from src.winrm.windows import WINRM_TRANSPORT
from src.util.ldap import LDAP
from src.winrm.task import Task, FAILURE_ACTION
from src.winrm.task_group import TaskGroup
from src.winrm.host import Host
from src.util.password_manager import PasswordManager, User
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
                
                async for i in ldap_conn.fetch_computers():
                    async for i in task_group.execute(Host(i), user):
                        print(json.dumps(i, indent=4))
                    #out, err, status = await cpu_task.execute(Host(i), user)
                    #if out is None:
                    #    info_dict["Hostname"] = i
                    #    info_dict["Error"] = status
                    #    info_dict["Username"] = user.username
                    #    info_dict["Transport"] = cpu_task.transport
                    #    info_dict["Script"] = cpu_task.script
                    #else:
                    #    name, caption, noc, nolp, _ = out.split('\r\n')
                    #    info_dict["Hostname"] = i
                    #    info_dict["CPU"] = {}
                    #    info_dict["CPU"]["Name"] = name
                    #    info_dict["CPU"]["Caption"] = caption
                    #    info_dict["CPU"]["Number of Cores"] = noc
                    #    info_dict["CPU"]["Number of Threads"] = nolp
                    #out, err, status = await os_task.execute(Host(i), user)
                    #if out is None:
                    #    info_dict["Hostname"] = i
                    #    info_dict["Error"] = status
                    #    info_dict["Username"] = user.username
                    #    info_dict["Transport"] = os_task.transport
                    #    info_dict["Script"] += os_task.script
                    #else:
                    #    caption, build_number, os_architecture, description, _ = out.split('\r\n')
                    #    info_dict["OS"] = {}
                    #    info_dict["OS"]["Version"] = caption
                    #    info_dict["OS"]["Build Number"] = build_number
                    #    info_dict["OS"]["Description"] = description
                    #    info_dict["OS"]["Architecture"] = os_architecture
                    #out, err, status = await net_task.execute(Host(i), user)
                    #if out is None:
                    #    info_dict["Hostname"] = i
                    #    info_dict["Error"] = status
                    #    info_dict["Username"] = user.username
                    #    info_dict["Transport"] = net_task.transport
                    #    info_dict["Script"] += net_task.script
                    #else:
                    #    ip_address, default_ip_gateway, description, index, dhcp_enabled, _ = out.split("\r\n")
                    #    info_dict["Networking"] = {}
                    #    info_dict["Networking"]["IP Address"] = ip_address
                    #    info_dict["Networking"]["Default Gateway"] = default_ip_gateway
                    #    info_dict["Networking"]["Description"] = description
                    #    info_dict["Networking"]["NIC Index"] = index
                    #    info_dict["Networking"]["DHCP Enabled"] = dhcp_enabled
                    #print(json.dumps(info_dict, indent=2))
                    
                        


if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main(sys.argv[1:]))