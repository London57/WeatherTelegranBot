from aiogram.fsm.state import State, StatesGroup

class GetWeather(StatesGroup):
    pre_city = State()
    city = State()
    day = State()
    