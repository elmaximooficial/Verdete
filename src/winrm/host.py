from enum import Enum

class WINRM_PROTOCOL(Enum):
    HTTP = 0
    HTTPS = 1

class WINRM_TRANSPORT(Enum):
    NTLM = 0
    KERBEROS = 1
    CERTIFICATE = 2

class Host:
    hostname : str
    port : int
    protocol : WINRM_PROTOCOL
    transport : WINRM_TRANSPORT
    
    def __init__(self, hostname : str,
                port : int = 5985,
                protocol : WINRM_PROTOCOL = WINRM_PROTOCOL.HTTP, 
                transport : WINRM_TRANSPORT = WINRM_TRANSPORT.NTLM):
        self.hostname = hostname
        self.port = port
        self.protocol = protocol
        self.transport = transport