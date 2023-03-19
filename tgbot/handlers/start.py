from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from tgbot.keyboards.reply import menu
#from .help import get_help
from loader import dp
from tgbot.keyboards.reply import menu
from tgbot.services.db_api.db_commands import *


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu)
    user = await add_user(user_id=message.from_user.id, full_name=message.from_user.full_name,
                          username=message.from_user.username)
    count = await count_users()
    await message.answer(
        '\n'.join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'Ты был занесен в базу',
                f'В базе <b>{count}</b> пользователей'

            ]
        )
    )
