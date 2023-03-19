from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='💲 Курс валют'), KeyboardButton(text='🌦 Погода')],
        [KeyboardButton(text='👤 Регистрация'), KeyboardButton(text='⚡️ Каталог')]
    ],
    resize_keyboard=True
)
