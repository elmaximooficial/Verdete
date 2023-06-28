from ldap3 import Connection, ASYNC, KERBEROS, SASL
from src.util.password_manager import User
from gssapi.raw.misc import GSSError
import toml
import asyncio
import os

class LDAP:
    __server : str
    __port : str
    __use_ssl : bool
    __user : User
    __base_dn : str
    __conn : Connection
    
    def __init__(self):
        """ Creates a new instance of LDAP based on the parameters set in 'config.toml'
        """
        self.__fetch_configuration()

    def __parse_server_name(self, name : str) -> str:
        for i in ['\\', '^', '~', '´', '`', '=', '+', '*', '?', '/', '{', '}', '[', ']', '(', ')', '%', '$', '#', '@', '!', '&', '¨', "'", '"']:
            if i in name:
                raise TypeError("Formatting of server name is invalid")
        return name
    
    def __parse_port(self, port : int) -> int:
        if port not in range(65535):
            raise TypeError("Invalid port number for server")
        return port

    def __parse_base_dn(self, base_dn : str) -> str:
        return base_dn.replace(' ', '')
    
    def __parse_user(self, user: str) -> str:
        for i in ['^', '~', '´', '`', '=', '+', '*', '?', '/', '{', '}', '[', ']', '(', ')', '%', '$', '#', '@', '!', '&', '¨', "'", '"']:
            if i in user:
                raise TypeError("Formatting of user name is invalid")
        return user

    def __fetch_configuration(self):
        try:
            absolute = os.path.dirname(__file__)
            relative = os.path.join(absolute, '../../resources/config.toml')
            with open(relative, 'r') as config_file:
                toml_file = toml.loads(config_file.read())
                if 'ldap' in toml_file.keys():
                    self.__server = self.__parse_server_name(toml_file['ldap']['server'])
                    
                    if toml_file['ldap']['port'] != None:
                        self.__port = self.__parse_port(toml_file['ldap']['port'])
                    elif toml_file['ldap']['use_ssl'] == False:
                        self.__port = 389
                    else:
                        self.__port = 636
                    
                    self.__base_dn = self.__parse_base_dn(toml_file['ldap']['base_dn'])
                    self.__use_ssl = toml_file['ldap']['use_ssl']
                    self.__user = self.__parse_user(toml_file['ldap']['user'])
                else:
                    print('Configuration file doesn\'t have information regarding the LDAP connection')
        except FileNotFoundError:
            print('Configuration file not found in path, the default path for this is /etc/verdete/config.toml')

    async def connect_to_server(self):
        """ Generate an Asynchronous connection to the LDAP server specified in 'config.toml'.
        As of this release, this method uses SASL with KERBEROS mechanism for authentication, you'll need to get a KRBTGT for the user
        with read privileges before using this.
            
        Returns:
            bool: Indicates if the connection was successful
        """
        try:
            self.__conn = Connection(self.__server, client_strategy=ASYNC, authentication=SASL, sasl_mechanism=KERBEROS)
            self.__conn.bind()
        except GSSError:
            print("You must get a KRBTGT first")
        return self.__conn.bound
        
    async def fetch_computers(self):
        """ This is a generator of computer names retrieved from LDAP after searching in the base_dn for the attribute 'dNSHostName' with filter
        (objectClass=Computer)

        Yields:
            str: dNSHostName of the computer in LDAP
        """
        message_id = self.__conn.search(self.__base_dn, '(objectClass=Computer)', attributes='dNSHostName')
        response, _ = self.__conn.get_response(message_id)
        for i in response:
            for key, value in i.items():
                if(key == "attributes"):
                    yield value['dNSHostName']
    async def dispose_connection(self):
        """ Unbinds the LDAP connection
        """
        self.__conn.unbind()
        
    def __str__(self):
        return str(self.__conn)