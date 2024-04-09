import asyncio

async def main(parser, i, result_dict={}, tasks=[]):
    functions_list = await parser.get_functions_list()
    for j in range(len(functions_list)):
        tasks.append(asyncio.create_task(functions_list[j](i)))
    for j in tasks:
        result_dict.update(await j)
    return result_dict



