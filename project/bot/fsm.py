from aiogram.fsm.state import State, StatesGroup

class GetWeather(StatesGroup):
    pre_city = State()
    city = State()
    pre_day = State()
    day = State()
    