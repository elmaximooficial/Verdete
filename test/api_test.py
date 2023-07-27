import sys
import os

sys.path.append(os.path.abspath('../'))

from src.api.fastapi_app import app
from src.api.winrm_host_groups import *
from src.api.winrm_task_group import *

print(app.state)

async def test_fetch_all_host_groups():
    print(await fetch_all_host_groups())
