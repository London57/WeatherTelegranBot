import asyncio
from .functions import list_of_func

async def main(i, result_dict={}, tasks=[]):
    for func in list_of_func:
        tasks.append(asyncio.create_task(func(i)))
    for j in tasks:
        result_dict.update(await j)
    return result_dict



