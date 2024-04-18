from aiogram import Router, types, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, StateFilter, and_f, Command
from aiogram.fsm.context import FSMContext
from .keyboards import get_days_keyboard, get_cities_keyboard
from .fsm import GetWeather
import asyncio
from .parsing.parsers import Parser
import requests
from .db.models import DataBase

dp = Dispatcher()

user_private_router = Router()

dp.include_router(user_private_router) 
 
db = DataBase()

@user_private_router.message(Command('go'))
async def start_bot(message: types.Message, state: FSMContext):
    cities = db.get_cities(user_id=message.from_user.id)
    keyboard = get_cities_keyboard(cities)
    await message.answer(
        'Введите название города, в котором хотите узнать погоду',
        reply_markup=keyboard,
        )
    
    await state.set_state(GetWeather.city)
 

@user_private_router.message(StateFilter(GetWeather.pre_city))
async def get_city(message: types.Message, state: FSMContext):
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
        await message.answer('Не удалось найти город')
        await get_city(message, state)
        return
    global parser
    

    db.insert_city(user_id=message.from_user.id, city=city)

    parser = Parser(city=city)

    keyboard = await asyncio.create_task(get_days_keyboard(parser))
    await message.answer(
        'Выберите день',
        reply_markup=keyboard,
        )
    await state.set_state(GetWeather.day)


@user_private_router.message(and_f(StateFilter(GetWeather.day), F.text == 'Отмена'))
async def return_to_city(message: types.Message, state: FSMContext):
    await state.set_state(GetWeather.pre_city)
    await get_city(message, state)


@user_private_router.message(StateFilter(GetWeather.day), F.text)
async def show_weather(message: types.Message, state: FSMContext):
    await state.update_data(day=message.text)
    data = await state.get_data()
    day_dict, day_list = await parser.get_days_dict_and_list()
    # !!!
    # if data['day'] not in day_list:
    #     await state.set_state(GetWeather.pre_day)
    #     ...
    
    res_data = await asyncio.create_task(parser.get_result_data(day=day_dict[data['day']]))
    await message.answer(str(res_data))
    await state.clear()
    await start_bot(message, state)
