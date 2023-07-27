import sys
import os

sys.path.append(os.path.abspath('../'))

from src.api.fastapi_app import app
import requests
import asyncio
import time
import threading
from multiprocessing.pool import ThreadPool

APP = 'http://localhost:8000'

def request(route: str):
    start = time.perf_counter()
    response = requests.get(APP + route)
    end = time.perf_counter()
    if response is None or response.status_code != 200:
        return end - start, response.status_code
    return end - start, 0

async def runner():
    times = []
    failure = []
    success = 0
    with ThreadPool() as pool:
        response = []
        for i in range(1000):
            response.append(pool.apply_async(func=request, args=["/"]))
        for i in response:
            i.wait()
            time, status = i.get()
            times.append(time)
            if status == 0:
                success += 1
            else:
                failure.append(status)

    print(f"MAX: {max(times)}\tMIN: {min(times)}\tAVG: {sum(times) / len(times)}\tSUM: {sum(times)}\n"
          f"ERROR: {len(failure)}\t\t\tSUCCESS: {success}\t\t\tERROR_CODES: {failure}")

async def run_task():
    response = requests.post(APP + '/winrmtask/Hostname/run/All')
    print(response.status_code)

asyncio.run(run_task())
