from aiogram import Router, types
from aiogram.filters import F, CommandStart


user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer('Введите название города, в котором хотите узнать погоду')

@user_private_router.message()
async def get_day(message: types.Message):
    ...