from aiogram import Router, types, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from .keyboards import keyboard, callback_query_dict
from .fsm import GetWeather
from parsing.parsing_data import main
import asyncio

dp = Dispatcher()

user_private_router = Router()

dp.include_router(user_private_router)


@user_private_router.message(StateFilter(None), CommandStart())
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите название города, в котором хотите узнать погоду',
        reply_markup=types.ReplyKeyboardRemove(),
        )
    await state.set_state(GetWeather.name)
 
@user_private_router.message(StateFilter(GetWeather.name), F.text)
async def get_day(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        'Выберите день',
        reply_markup=keyboard,
        )
    await state.set_state(GetWeather.day)

@user_private_router.message(StateFilter(GetWeather.day), F.text)
async def show_weather(message: types.Message, state: FSMContext):
    await state.update_data(day=message.text)
    data = await state.get_data()
    # weather = loop.main(callback_query_dict[data['day']])
    # loop = asyncio.new_event_loop()
    # res = loop.run_until_complete(main(2))
    # loop.close()
    # await message.answer(str(res))

    #
    ...
    await state.clear()
