from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


async def get_days_keyboard(parser, tasks=[], day_list=[]):
    
    for i in range(8):
        tasks.append(asyncio.create_task(parser.dates_to_keyboard(i)))
        
    for task in tasks:
        day_list.append(await task)
   

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=day_list[i]) for i in range(4)
            ],
            [
                KeyboardButton(text=day_list[i]) for i in range(4, 8)
            ],
            [
                KeyboardButton(text='Отмена'),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
        



def get_cities_keyboard(cities):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=cities[i]) for i in range(len(cities))
            ],
        ],
        resize_keyboard=True
    )
    return keyboard