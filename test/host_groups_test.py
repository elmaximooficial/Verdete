import sys
import os

sys.path.append(os.path.abspath('../'))

from src.winrm.host_group import Host, HostGroup
from src.util.password_manager import User
from src.injector.ldap_injector import LDAPInjector
from src.winrm.task_group import WinRMTaskGroup, WinRMTask
import asyncio


async def main():
    ldap_conn = LDAPInjector()
    await ldap_conn.connect_to_server()

    print("Creating Host Group in Test")
    test_group = await HostGroup.fetch_hostgroup(name="All")
    cpd_group = await HostGroup.create_hostgroup(name="CPD")
    async for i in cpd_group:
        print(i)
    print("Created Host Group")
    task_group = await WinRMTaskGroup.fetch_task(name="Hostname")
    await task_group.execute(group=test_group, debug=False)

if __name__ == "__main__":
    asyncio.run(main())
