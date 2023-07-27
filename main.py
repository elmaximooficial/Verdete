from src.trigger.timer_trigger import TimerTrigger
from threading import Thread
import asyncio
import sys
from src.api.fastapi_app import *
from prometheus_client import Counter

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
        timer = TimerTrigger()
        timer_thread = Thread(name="Timer", target=timer.start, daemon=True)
        timer_thread.start()


if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main(sys.argv[1:]), debug=False)
