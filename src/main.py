from bot.bot import bot
import asyncio
from bot.handlers import dp
from bot.db.database import DataBase
from bot.db.init_db import init_db


ALLOWED_UPDATES = ['message']

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    init_db()
    asyncio.run(main())