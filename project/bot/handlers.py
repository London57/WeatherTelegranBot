from aiogram import Router, types, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from .keyboards import get_keyboard
from .fsm import GetWeather
import asyncio
from .parsing.parser import Parser
import requests

dp = Dispatcher()

user_private_router = Router()

dp.include_router(user_private_router)


@user_private_router.message(or_f(StateFilter(GetWeather.pre_city), CommandStart()))
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите название города, в котором хотите узнать погоду',
        reply_markup=types.ReplyKeyboardRemove(),
        )
    
    await state.set_state(GetWeather.city)
 
@user_private_router.message(StateFilter(GetWeather.city), F.text)
async def get_day(message: types.Message, state: FSMContext):
    
    await state.update_data(city=message.text)
    status_data = await state.get_data()
    city = status_data['city'].lower()
    if requests.get(f'https://pogoda.mail.ru/prognoz/{city}/').status_code == 404:
        await state.set_state(GetWeather.pre_city)
        await message.answer('Не удалось найти город, попробуйте ещё раз')
        return
    global parser
    
    parser = Parser(city=city)
   
    keyboard = await asyncio.create_task(get_keyboard(parser))
    await message.answer(
        'Выберите день',
        reply_markup=keyboard,
        )
    await state.set_state(GetWeather.day)


@user_private_router.message(StateFilter(GetWeather.day), F.text == 'Отмена')
async def return_to_city(message: types.Message, state: FSMContext):
    await state.set_state(GetWeather.pre_city)
    await message.answer('Введите название города, в котором хотите узнать погоду',)


@user_private_router.message(StateFilter(GetWeather.day), F.text)
async def show_weather(message: types.Message, state: FSMContext):
    await state.update_data(day=message.text)
    data = await state.get_data()

    day_dict, _ = await parser.get_days_dict_and_list()
    res_data = await asyncio.create_task(parser.get_result_data(day=day_dict[data['day']]))
    # res_data = await asyncio.create_task(main(callback_query_dict[data['day']]))
    await message.answer(str(res_data))
    
    # await state.clear()
