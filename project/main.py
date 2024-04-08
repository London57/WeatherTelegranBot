from project.bot.bot import bot
import asyncio
from project.bot.handlers import dp


ALLOWED_UPDATES = ['message']

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())