from winrm.protocol import Protocol
from winrm import Response
from src.util.password_manager import User
from enum import StrEnum
from src.winrm.host import Host
from winrm.exceptions import *
from requests.exceptions import *
from base64 import b64encode
import warnings

class WINRM_TRANSPORT(StrEnum):
    NTLM = "ntlm"
    KERBEROS = "kerberos"


async def create_connection(host : Host, user : User, transport : WINRM_TRANSPORT) -> (str | None):
    if type(host.hostname) != str:
        print(f"Computer name must be a string! {host.hostname}")
    try:
        conn = Protocol (
            endpoint=f'http://{host.hostname}:{host.port}/wsman',
            transport=transport,
            username=user.username,
            password=user.password,
            server_cert_validation='ignore',
            operation_timeout_sec=15,
            read_timeout_sec=360
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
    except InvalidURL:
        return (False, None, "Invalid URL")

async def execute_command (host : Host, user : User, command : str, transport : WINRM_TRANSPORT, conn : Protocol, shell_id : str) -> tuple:
    try:
        encoded = b64encode(command.encode('utf_16_le')).decode('ascii')
        command_id = conn.run_command(shell_id, 'powershell -encodedcommand {0}'.format(encoded))
        try:
            rs = Response(conn.get_command_output(shell_id, command_id))
        except ReadTimeout:
            return (command_id, None, "Read Timeout")
        return (command_id, rs.std_out.decode('cp860'), rs.std_err.decode('cp860').strip(), rs.status_code)
    except WinRMError:
        return(None, host.hostname, "The system couldn't find the specified file", "")
    
async def dispose_shell(shell_id : str, command_id, connection : Protocol):
    connection.cleanup_command(shell_id, command_id)
    connection.close_shell(shell_id)