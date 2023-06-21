import asyncio
import sys, getopt
from src.winrm.windows import WinRM
from src.util.ldap import LDAP
from src.util.password_manager import PasswordManager, User
from getpass import getpass

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
        opts, args = getopt.getopt(argv, '', ['fetch-computers', 'gen-password=', 'gen-key', 'query-computers='])
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
                ldap_conn = LDAP.fetch_configurations()
                ldap_conn.do_connect_to_server()
                username = input('Insert the Username: ')
                password = getpass('Insert the Password: ')
                pass_manager = PasswordManager.load_key()
                
                user = User()
                user.username = username
                user.password = password
                
                winrm = WinRM()
                
                computers = ['PM-CPDADM001', 'PM-CPDADM002', 'PM-CPDADM003', 'PM-CPDADM004', 'PM-SAFCPD007', 'ADM002', 'PM-NOTEINFO99']
                
                for i in computers:
                    std_out, std_err, result_code = winrm.do_query_computer(i, user, arg)
                    with open('result', 'a') as file:
                        try:
                            file.write(i + std_out)
                        except TypeError:
                            pass
                    print(std_out)
                    print(std_err)
                
                #loop = asyncio.get_event_loop()
                #loop.run_in_executor(None, winrm.query_these_computers(computers1, user, 'Restart-PostgreSQL
                #for i in pending:
                #    i.cancel()
                #group = asyncio.gather(*pending, return_exceptions=True)
                #loop.run_until_complete(group)
                #loop.close()
                
                for key, value in winrm.errors.items():
                    print(key + ':\t' + value)


if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main(sys.argv[1:]))