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
from resources.wmi import task_group
from multiprocessing import Process
from random import Random
import time

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

                wmi_check = lambda x: x != None
                availability_task = Task(name="Availability",
                                         script='hostname',
                                         script_checking=wmi_check,
                                         script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                                         transport=WINRM_TRANSPORT.NTLM)
                available = HostGroup(name="Available", description="All Available Hosts")
                avail_tg = TaskGroup(availability_task, transport=WINRM_TRANSPORT.NTLM)
                db_handler = DBHandler()
                db_handler.connect('Hosts')
                computers = HostGroup(name="All", description="All Computers")
                async for j in ldap_conn.fetch_computers():
                    computers.hosts.append(Host(j))
                #async with asyncio.TaskGroup() as tg:
                async for j in computers:
                 #       task = tg.create_task(
                    await task_group.execute(host=j, user=user, db_handler=db_handler, debug=False)
if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main(sys.argv[1:]), debug=False)