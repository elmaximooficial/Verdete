from winrm.protocol import Protocol
from src.util.password_manager import User
from enum import StrEnum
from src.winrm.host import Host
from winrm.exceptions import *
from requests.exceptions import *

class WINRM_TRANSPORT(StrEnum):
    NTLM = "ntlm"
    KERBEROS = "kerberos"


async def create_connection(host : Host, user : User, transport : WINRM_TRANSPORT) -> (str | None):
    if type(host.hostname) != str:
        raise TypeError("Computer name must be a string!")
    try:
        conn = Protocol (
            endpoint=f'http://{host.hostname}:{host.port}/wsman',
            transport=transport,
            username=user.username,
            password=user.password,
            server_cert_validation='ignore',
            operation_timeout_sec=5,
            read_timeout_sec=10
        )
        return (True, conn, conn.open_shell())
    except ConnectionError:
        return (False, None, "No route to host")
    except InvalidCredentialsError:
        return (False, None, "Invalid Credentials")
    except ReadTimeout:
        return (False, None, "Read Timeout")
    except WinRMOperationTimeoutError:
        return (False, None, "Operation Timeout")

async def execute_command (host : Host, user : User, command : str, transport : WINRM_TRANSPORT, conn : Protocol, shell_id : str) -> tuple:
    command_id = conn.run_command(shell_id, command)
    std_out, std_err, status_code = conn.get_command_output(shell_id, command_id)
    return (command_id, std_out.decode('cp860'), std_err.decode('cp860').strip(), status_code)

async def dispose_shell(shell_id : str, command_id, connection : Protocol):
    connection.cleanup_command(shell_id, command_id)
    connection.close_shell(shell_id)