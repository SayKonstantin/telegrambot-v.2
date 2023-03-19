from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    name = State()
    age = State()
    gender = State()
    email = State()


class WeatherState(StatesGroup):
    where = State()
