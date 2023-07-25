import sys
import os

sys.path.append(os.path.abspath('../'))

from src.winrm.host_group import Host, HostGroup
from src.util.password_manager import User
from src.util.ldap import LDAP
from src.winrm.task_group import WinRMTaskGroup, WinRMTask
import asyncio


async def main():
    ldap_conn = LDAP()
    await ldap_conn.connect_to_server()

    print("Creating Host Group in Test")
    test_group = await HostGroup.fetch_hostgroup(
        hosts=[Host(i) async for i in ldap_conn.fetch_computers()],
        name="All",
        description="All Hosts",
        user=User("PA\Administrador", "¨TF6yh7uj"))
    print("Created Host Group")
    task_group = WinRMTaskGroup(WinRMTask("Hostname", '"`nhostname`n$(hostname)"'))
    await task_group.execute(group=test_group, debug=False)

if __name__ == "__main__":
    asyncio.run(main())
