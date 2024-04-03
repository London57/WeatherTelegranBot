from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.filters import CommandStart

from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())


ALLOWED_UPDATES = ['message']
bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
