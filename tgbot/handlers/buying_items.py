from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup, ContentType
from asgiref.sync import sync_to_async

from django_project.telegrambot.items.models import Purchase
from loader import dp

from tgbot.keyboards.inline import buy_item
from tgbot.keyboards.reply import menu
from tgbot.services.db_api.db_commands import select_user, get_item


@dp.callback_query_handler(buy_item.filter())
async def enter_buy(call: CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = callback_data.get('item_id')
    user = await select_user(call.from_user.id)
    item = await get_item(item_id)
    purchase = Purchase()
    purchase.buyer_id = user.id
    purchase.item_id_id = int(item_id)
    purchase.receiver = call.from_user.full_name
    await state.update_data(purchase=purchase, item=item)
    await call.message.answer('Введите количество')
    await state.set_state('enter_quantity')


@dp.message_handler(state='enter_quantity')
async def enter_quantity(message: Message, state: FSMContext):
    quantity = message.text
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer('Неверное значение, введите заново')
        return
    async with state.proxy() as data:
        data['purchase'].quantity = quantity
        data['purchase'].amount = quantity * data['item'].price

    await message.answer('Пришлите свой телефон', reply_markup=ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton('Прислать телефон', request_contact=True)
        ]], resize_keyboard=True
    ))
    await state.set_state('enter_phone')


@dp.message_handler(state='enter_phone', content_types=ContentType.CONTACT)
async def enter_phone(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    data = await state.get_data()
    purchase = data.get('purchase')
    purchase.phone_number = phone_number
    await sync_to_async(purchase.save)()
    await message.answer('Покупка создана. Скоро вам позвонит менеджер!', reply_markup=menu)
    await state.reset_state()
