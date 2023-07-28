import asyncio
import concurrent.futures
import datetime

from pandas import read_table, read_json, read_xml, DataFrame
from io import StringIO
from functools import partial
from __future__ import annotations
from typing import *


class TaskFormatter:

    def __init__(self):
        pass

    @staticmethod
    async def csv_to_dict(data: str = None, file: str = None) -> dict[str, Any]:
        parsed: DataFrame = await asyncio.to_thread(partial(read_table,
                                                            filepath_or_buffer=file if file else StringIO(data),
                                                            delimiter=',',
                                                            engine='pyarrow'))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
            return await asyncio.get_running_loop().run_in_executor(exe, partial(parsed.to_dict, orient='records'))

    @staticmethod
    async def json_to_dict(data: str = None, file: str = None) -> dict[str, Any]:
        parsed: DataFrame = await asyncio.to_thread(partial(read_json,
                                                            filepath_or_buffer=file if file else StringIO(data)))
        return await asyncio.to_thread(partial(parsed.to_dict, orient='records'))

    @staticmethod
    async def xml_to_dict(data: str = None, file: str = None) -> dict[str, Any]:
        parsed: DataFrame = await asyncio.to_thread(partial(read_xml,
                                                            filepath_or_buffer=file if file else StringIO(data)))
        return await asyncio.to_thread(partial(parsed.to_dict, orient='records'))

    @staticmethod
    async def ps_table_to_dict(data: str) -> dict[str, Any]:
        parsed: DataFrame = await asyncio.to_thread(partial(read_table,
                                                            filepath_or_buffer=StringIO(data),
                                                            delimiter='\t'))
        return await asyncio.to_thread(partial(parsed.to_dict, orient='records')[1:])
