from src.util.ldap import LDAP
from src.util.password_manager import PasswordManager, User
from src.util.timer import Timer
from src.winrm.host_group import HostGroup, Host
from src.winrm.task_group import WinRMTaskGroup, WinRMTask
from getpass import getpass
from threading import Thread
import asyncio
import sys, getopt

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


class Main:
    async def main(self, argv):
        timer = Timer()
        timer_thread = Thread(name="Timer", target=timer.start, daemon=True)
        timer_thread.start()

        opts, args = getopt.getopt(argv, '', ['fetch-computers', 'gen-password=', 'gen-key', 'query-computers', 'debug'])
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
                all = HostGroup(name="All", description="All Hosts from LDAP", user=user)
                async for i in ldap_conn.fetch_computers():
                    all.add_host(Host(hostname=i))

                task_group = WinRMTaskGroup(WinRMTask("CPU", "Get-WMIObject Win32_Processor | "
                                                             "Select name, manufacturer, description | "
                                                             "ConvertTo-Csv"))
                await task_group.execute(group=all, debug=True)

if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main(sys.argv[1:]), debug=False)