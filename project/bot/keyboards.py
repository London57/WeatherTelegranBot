from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from parsing.functions import dates
import asyncio


async def get_dates(tasks=[], day_list=[]):
    for i in range(7):
        tasks.append(asyncio.create_task(dates(i)))
    print(tasks)
    #create task for today day here
    for task in tasks:
        day_list.append(await task)
    return day_list

loop = asyncio.new_event_loop()
day_list = loop.run_until_complete(get_dates())
loop.close()

callback_query_dict = {day_list[i]: i for i in range(7)}
# day:number

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
