from aiogram import Router, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, StateFilter, and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import asyncio
from .keyboards import get_days_keyboard, get_cities_keyboard
from .fsm import GetWeather
from .parsing.parser import Parser, city_not_found
from .db.services import CityRepositoryService
from .db.init_db import create_db_model


dp = Dispatcher()
repo = CityRepositoryService(create_db_model())


@dp.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):

    cities = repo.get_cities(user_id=message.from_user.id)
    print(cities)
    keyboard = get_cities_keyboard(cities)
    await message.answer(
        'Введите название города, в котором хотите узнать погоду',
        reply_markup=keyboard,
        )
    print('ffffffffffff')
    await state.set_state(GetWeather.city)
 

@dp.message(StateFilter(GetWeather.pre_city))
async def get_city(message: Message, state: FSMContext):
    cities = repo.get_cities(user_id=message.from_user.id)
    cities_keyboard = get_cities_keyboard(cities)
    print('__________________')
    await message.answer(
        'Введите название города, в котором хотите узнать погоду',
        reply_markup=cities_keyboard,
        )
       
    await state.set_state(GetWeather.city)

@dp.message(StateFilter(GetWeather.city), F.text)
async def get_day(message: Message, state: FSMContext):
    city = message.text.lower()
    await state.update_data(city=city)

    if city_not_found(city):
        await state.set_state(GetWeather.pre_city)
        await message.answer('Не удалось найти город')
        return

    global parser
    parser = Parser(city=city)

    global days_keyboard
    days_keyboard = await asyncio.create_task(get_days_keyboard(parser))

    await message.answer(
        'Выберите день',
        reply_markup=days_keyboard,
        )
    
    repo.insert_city(user_id=message.from_user.id, city=city)
    await state.set_state(GetWeather.day)

@dp.message(and_f(StateFilter(GetWeather.day), F.text == 'Отмена'))
async def return_to_get_city(message: Message, state: FSMContext):
    await state.set_state(GetWeather.pre_city)
    await get_city(message, state)


@dp.message(StateFilter(GetWeather.day), F.text)
async def show_weather(message: Message, state: FSMContext):
    await state.update_data(day=message.text)

    data = await state.get_data()
    day_dict, day_list = await parser.get_days_dict_and_list()
    if data['day'] not in day_list:
        await get_day_exc(message, state)
        return
    
    res_data = await asyncio.create_task(parser.get_result_data(day=day_dict[data['day']]))
    await message.answer(str(res_data))
    await state.clear()
    await start_bot(message, state)


@dp.message(StateFilter(GetWeather.pre_day))
async def get_day_exc(message: Message, state: FSMContext):
    await message.answer(
        'Неверно указан день',
        reply_markup=days_keyboard
    )
    print(message.text)
    await state.set_state(GetWeather.day)
    