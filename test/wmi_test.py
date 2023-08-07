import sys
import os

sys.path.append(os.path.abspath('../'))

from src.winrm.wmi_task_group import WINRM_TRANSPORT, WINRM_PROTOCOL, WinRMConnection, WMITaskGroup
from src.winrm.host_group import HostGroup, Host
from src.injector.ldap_injector import LDAPInjector
from src.util.password_manager import User
import asyncio

async def execute():
    host_group = await HostGroup.fetch_hostgroup(name="All")
    task = WMITaskGroup()
    await task.execute(group=host_group)

if __name__ == '__main__':
    asyncio.run(execute())