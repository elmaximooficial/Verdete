from winrm.protocol import Protocol
from winrm.exceptions import InvalidCredentialsError, WinRMOperationTimeoutError
from requests.exceptions import ConnectionError, ReadTimeout, InvalidURL
from src.util.password_manager import User
from src.util.ldap import LDAP
import asyncio

class WinRM:
    errors : dict
    successes : set

    def __init__(self):
        self.errors = {}
        self.successes = set()

    def query_these_computers(self, computers : set, user : User, command : str) -> tuple:
        for i in computers:
            self.do_query_computer(i, user, command)

    def query_all_computers(self, ldap_conn : LDAP, user : User, command : str):
        for i in ldap_conn.fetch_computers():
            self.do_query_computer(i, user, command)
            
    def do_query_computer(self, computer_name : str, user : User, command : str) -> tuple:
        print(computer_name)
        if type(computer_name) == str:
            conn = Protocol(
                endpoint=f'http://{computer_name}:5985/wsman',
                transport='ntlm',
                username=user.username,
                password=user.password,
                server_cert_validation='ignore',
                operation_timeout_sec=5,
                read_timeout_sec=10
            )
            try:
                shell_id = conn.open_shell()
                command_id = conn.run_command(shell_id, command)
                std_out, std_err, status_code = conn.get_command_output(shell_id, command_id)
                conn.cleanup_command(shell_id, command_id)
                conn.close_shell(shell_id)
                self.successes.add(computer_name)
                return (std_out.decode('cp860'), std_err.decode('cp860'), status_code)
            except ConnectionError as e:
                print(f'Couldn\'t connect to {computer_name}')
                self.errors[computer_name] = str(e)
                return (None, None, None)
            except InvalidCredentialsError as e:
                print(f'Credentials for {user.username} was rejected by {computer_name}')
                self.errors[computer_name] = str(e)
                return (None, None, None)
            except ReadTimeout as e:
                print(f'Connection timeout for computer {computer_name}')
                self.errors[computer_name] = str(e)
                return (None, None, None)
            except InvalidURL as e:
                print(f"Invalid URL for {computer_name}")
                self.errors[computer_name] = str(e)
                return (None, None, None)
            except WinRMOperationTimeoutError as e:
                print(f"Timeout on computer {computer_name}")
                self.errors[computer_name] = str(e)
                return (None, None, None)