from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


async def get_keyboard(parser, tasks=[], day_list=[]):
    
    for i in range(7):
        tasks.append(asyncio.create_task(parser.dates(i)))
        
    #create task for today day here
    for task in tasks:
        day_list.append(await task)
    # loop = asyncio.get_event_loop()
    # courotine = loop.create_task(get_dates())
    # day_list = loop.run_until_complete(courotine)
    # global callback_query_dict
    # callback_query_dict = {day_list[i]: i for i in range(7)}

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=day_list[0]),
                KeyboardButton(text=day_list[1]),
                KeyboardButton(text=day_list[2]),
            ],
            [
                KeyboardButton(text=day_list[3]),
                KeyboardButton(text=day_list[4]),
                KeyboardButton(text=day_list[5]),
                KeyboardButton(text=day_list[6]),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
        



