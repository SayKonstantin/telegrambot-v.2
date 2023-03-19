import asyncio
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, ContentType, InputFile
from aiogram.dispatcher.filters import Command, Text
from asgiref.sync import sync_to_async
from django_project.telegrambot.telegrambot.settings import MEDIA_ROOT
from django_project.telegrambot.items.models import Purchase
from tgbot.keyboards.inline import categories_keyboard, subcategories_keyboard, items_keyboard, item_keyboard, catalog, \
    buy_item
from loader import dp
from tgbot.services.db_api.db_commands import get_item, select_user


@dp.message_handler(Command('menu') | Text(equals='⚡️ Каталог'))
async def show_menu(message: Message):
    await list_categories(message)


async def list_categories(message: Union[Message, CallbackQuery], **kwargs):
    markup = await categories_keyboard()
    if isinstance(message, Message):
        await message.answer('Смотри, что у нас есть', reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await callback.message.edit_reply_markup(markup)


async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category=category, subcategory=subcategory)
    await callback.message.edit_text('Смотри, что у нас есть', reply_markup=markup)


async def show_item(callback: CallbackQuery, category, subcategory, item_id):
    markup = item_keyboard(category, subcategory, item_id)
    item = await get_item(item_id)
    text = f'Товар {item}'
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.message.answer_photo(InputFile(MEDIA_ROOT + '/' + str(item.image)), caption=item.description)


@dp.callback_query_handler(catalog.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = int(callback_data.get('item_id'))
    levels = {
        '0': list_categories,
        '1': list_subcategories,
        '2': list_items,
        '3': show_item
    }
    current_level_function = levels[current_level]
    await current_level_function(call, category=category, subcategory=subcategory, item_id=item_id)


