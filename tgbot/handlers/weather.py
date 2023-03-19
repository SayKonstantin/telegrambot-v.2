import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from tgbot.keyboards.reply import menu
from loader import dp
from requests import request
import json
from json.decoder import JSONDecodeError
from tgbot.config import load_config
from enum import Enum
from dataclasses import dataclass
from typing import TypeAlias
from tgbot.misc.states import WeatherState


class WeatherType(Enum):
    CLEAR = 'Ясно'
    PARTLY_CLOUDY = 'Малооблачно'
    CLOUDY = 'Облачно с прояснениями'
    OVERCAST = 'Пасмурно'
    DRIZZLE = 'Морось'
    LIGHT_RAIN = 'Небольшой дождь'
    RAIN = 'Дождь'
    MODERATE_RAIN = 'Умеренно сильный дождь'
    HEAVY_RAIN = 'Сильный дождь'
    CONTINUOUS_HEAVY_RAIN = 'Длительный сильный дождь'
    SHOWERS = 'Ливень'
    WET_SNOW = 'Дождь со снегом'
    LIGHT_SNOW = 'Небольшой снег'
    SNOW = 'Снег'
    SNOW_SHOWERS = 'Снегопад'
    HAIL = 'Град'
    THUNDERSTORM = 'Гроза'
    THUNDERSTORM_WITH_RAIN = 'Дождь с грозой'
    THUNDERSTORM_WITH_HAIL = 'Гроза с градом'


Celsius: TypeAlias = float


@dataclass
class Weather:
    temperature: Celsius
    condition: WeatherType
    wind_speed: float
    humidity: float


def parse_temperature(openweather_dict: dict) -> Celsius:
    return openweather_dict['temp']


def parse_condition(openweather_dict: dict) -> WeatherType:
    weather_kind: str = openweather_dict['condition']
    weather_types = {
        'clear': WeatherType.CLEAR,
        'partly-cloudy': WeatherType.PARTLY_CLOUDY,
        'cloudy': WeatherType.CLOUDY,
        'overcast': WeatherType.OVERCAST,
        'drizzle': WeatherType.DRIZZLE,
        'light-rain': WeatherType.LIGHT_RAIN,
        'rain': WeatherType.RAIN,
        'moderate-rain': WeatherType.MODERATE_RAIN,
        'heavy-rain': WeatherType.HEAVY_RAIN,
        'continuous-heavy-rain': WeatherType.CONTINUOUS_HEAVY_RAIN,
        'showers': WeatherType.SHOWERS,
        'wet-snow': WeatherType.WET_SNOW,
        'light-snow': WeatherType.LIGHT_SNOW,
        'snow': WeatherType.SNOW,
        'snow-showers': WeatherType.SNOW_SHOWERS,
        'hail': WeatherType.HAIL,
        'thunderstorm': WeatherType.THUNDERSTORM,
        'thunderstorm-with-rain': WeatherType.THUNDERSTORM_WITH_RAIN,
        'thunderstorm-with-hail': WeatherType.THUNDERSTORM_WITH_HAIL
    }
    for _type, _weather_type in weather_types.items():
        if weather_kind.startswith(_type):
            return _weather_type


def parse_wind_speed(openweather_dict: dict) -> float:
    return openweather_dict['wind_speed']


def parse_humidity(openweather_dict: dict) -> float:
    return openweather_dict['humidity']


@dp.message_handler(Command('weather') | Text(equals='🌦 Погода'))
async def show_button(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    button_cancel = types.KeyboardButton(text="Отмена")
    keyboard.add(button_geo, button_cancel)
    await message.answer("Где находишься?", reply_markup=keyboard)
    await WeatherState.where.set()


@dp.message_handler(state=WeatherState.where)
async def hide_location_button(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.reset_state()
        await message.answer(f'Ок', reply_markup=menu)
    else:
        await message.answer('Дай точку на карте')


@dp.message_handler(content_types=["location"], state=WeatherState.where)
async def get_weather(message: types.Message, state: FSMContext):
    if message.location is not None:
        weather = await make_request(message.location.longitude, message.location.latitude)
        await message.answer(text=f'Сейчас {weather.temperature}℃\n'
                                  f'{weather.condition.value}\n'
                                  f'Скорость ветра {weather.wind_speed} м/с\n'
                                  f'Влажность воздуха {weather.humidity} %',
                             reply_markup=menu)
        await state.reset_state()


async def make_request(longitude: float, latitude: float) -> Weather:
    url = f"https://api.weather.yandex.ru/v2/informers?lat={latitude}&lon={longitude}&extra=true"
    headers = {'X-Yandex-API-Key': load_config().yandex_weather.token}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            json_body = await r.json()
    print(json_body)
    try:
        openweather_dict = json_body['fact']
    except JSONDecodeError:
        raise SystemError

    print(openweather_dict)
    return Weather(temperature=parse_temperature(openweather_dict),
                   condition=parse_condition(openweather_dict),
                   wind_speed=parse_wind_speed(openweather_dict), humidity=parse_humidity(openweather_dict))
