import asyncio
import concurrent.futures

from pandas import read_table, read_json, read_xml
from io import StringIO
from functools import partial


class TaskFormatter:

    def __init__(self):
        pass

    @staticmethod
    async def csv_to_dict(data: str = None, file: str = None):
        parsed = await asyncio.to_thread(partial(read_table,
                                                 filepath_or_buffer=file if file else StringIO(data),
                                                 delimiter=',',
                                                 engine='pyarrow'))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
            return await asyncio.get_running_loop().run_in_executor(exe, partial(parsed.to_dict, orient='records'))

    @staticmethod
    async def json_to_dict(data: str = None, file: str = None):
        parsed = [await asyncio.to_thread(partial(read_json,
                                                 filepath_or_buffer=file if file else StringIO(record))) for record in data]
        return [await asyncio.to_thread(partial(i.to_dict, orient='records')) for i in parsed]

    @staticmethod
    async def xml_to_dict(data: str = None, file: str = None):
        parsed = await asyncio.to_thread(partial(read_xml,
                                                 filepath_or_buffer=file if file else StringIO(data)))
        return await asyncio.to_thread(partial(parsed.to_dict, orient='records'))

    @staticmethod
    async def ps_table_to_dict(data: str):
        parsed = await asyncio.to_thread(partial(read_table,
                                                 filepath_or_buffer=StringIO(data),
                                                 delimiter='\t'))
        return await asyncio.to_thread(partial(parsed.to_dict, orient='recordes')[1:])
