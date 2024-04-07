from aiogram.fsm.state import State, StatesGroup

class GetWeather(StatesGroup):
    name = State()
    day = State()
    