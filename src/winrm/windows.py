import concurrent.futures

from winrm.protocol import Protocol
from winrm import Response
from enum import StrEnum
from base64 import b64encode
from winrm.exceptions import *
from requests.exceptions import *
import asyncio
import asyncio.threads
import functools


class WINRM_TRANSPORT(StrEnum):
    NTLM = "ntlm"
    KERBEROS = "kerberos"


class WINRM_PROTOCOL(StrEnum):
    HTTP = "http"
    HTTPS = "https"


class WinRMConnection(Protocol):
    """
    This represents a connection to a remote host, having methods for executing commands, as well as disposing the connection.
    This object contains the state of the connection, be careful to keep track of this resource, use in context manager
    or close every opened shell.
    """
    shell_id: str = None
    hostname: str = None

    async def execute_ps(self, encoded: str):
        """
        Executes the 'encoded' command in the remote host represented by this object via the PowerShell
        :param encoded: The command to be executed, encoded in utf_16_le and ascii, user WinRMConnection.encode_command()
        for generating this parameter
        :return: The decoded result in the form of a tuple, containing the std_out, std_err and status_code
        """
        try:
            command_id = await asyncio.get_running_loop().run_in_executor(None,
                                                                          functools.partial(self.run_command,
                                                                                            shell_id=self.shell_id,
                                                                                            command='powershell -encodedcommand {0}'.format(encoded)))
            command_output = await asyncio.get_running_loop().run_in_executor(None,
                                                                              functools.partial(self.get_command_output,
                                                                                                      shell_id=self.shell_id,
                                                                                                      command_id=command_id))
            rs = Response(command_output)
            return rs.std_out.decode('cp860'), rs.std_err.decode('cp860'), rs.status_code
        except ConnectionError:
            print(f"Could not connect to {self.transport.endpoint}")
        except InvalidURL:
            print(f"Invalid URL {self.transport.endpoint}")
        except InvalidCredentialsError:
            print(f"Invalid Credentials for host {self.transport.endpoint}")
        except WinRMError as e:
            print(f"WinRM Error {e}")
        except WinRMOperationTimeoutError:
            print(f"Connection Timed out for host {self.transport.endpoint}")
        except ReadTimeout:
            print(f"Read Time out for host {self.transport.endpoint}")

    async def execute_cmd(self, command: str):
        """
        Executes the 'command' in the remote host represented by this object via the Command Prompt
        :param command: The raw command to be executed
        :return: The decoded result in the form of a tuple, containing the std_out, std_err and status_code
        """
        try:
            command_id = await asyncio.get_running_loop().run_in_executor(None,
                                                                          functools.partial(self.run_command,
                                                                                            shell_id=self.shell_id,
                                                                                            command=command))
            command_output = await asyncio.get_running_loop().run_in_executor(None,
                                                                              functools.partial(self.get_command_output,
                                                                                                shell_id=self.shell_id,
                                                                                                command_id=command_id))
            rs = Response(command_output)
            return rs.std_out.decode('cp860'), rs.std_err.decode('cp860'), rs.status_code
        except ConnectionError:
            print(f"Could not connect to {self.transport.endpoint}")
        except InvalidURL:
            print(f"Invalid URL {self.transport.endpoint}")
        except InvalidCredentialsError:
            print(f"Invalid Credentials for host {self.transport.endpoint}")
        except WinRMError as e:
            print(f"WinRM Error {e}")
        except WinRMOperationTimeoutError:
            print(f"Connection Timed out for host {self.transport.endpoint}")
        except ReadTimeout:
            print(f"Read Time out for host {self.transport.endpoint}")

    async def connect(self):
        """
        Tries to connect to the remote host represented by this object, the main operation 'open_shell' executes in a
        ThreadPoolExecutor
        """
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
                self.shell_id = await asyncio.get_running_loop().run_in_executor(exe, self.open_shell)
                self.hostname = self.transport.endpoint
                print(f"Connected to {self.transport.endpoint}")
        except ConnectionError:
            print(f"Could not connect to {self.transport.endpoint}")
        except InvalidURL:
            print(f"Invalid URL {self.transport.endpoint}")
        except InvalidCredentialsError:
            print(f"Invalid Credentials for host {self.transport.endpoint}")
        except WinRMError as e:
            print(f"WinRM Error {e}")
        except WinRMOperationTimeoutError:
            print(f"Connection Timed out for host {self.transport.endpoint}")
        except ReadTimeout:
            print(f"Read Time out for host {self.transport.endpoint}")

    async def dispose(self):
        """
        Closes the remote shell opened for this object, be careful not to try and close a shell that has not been opened,
        for example in the case the connect() command finds an exception.
        The main operation for this function - 'close_shell' - is run in a ThreadPoolExecutor
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
            await asyncio.get_running_loop().run_in_executor(exe, functools.partial(self.close_shell, shell_id=self.shell_id))

    async def __aenter__(self):
        """
        Calls self.connect()
        :return: WinRMConnection object in the connected state
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        calls self.dispose()
        """
        await self.dispose()

    @staticmethod
    def encode_command(command):
        """
        Return the 'command' as string encoded in utf_16_le and ascii. This is useful for executing powershell commands
        :param command: The raw command
        :return: encoded string
        """
        return b64encode(command.encode('utf_16_le')).decode('ascii')