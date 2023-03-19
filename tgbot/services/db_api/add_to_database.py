import asyncio

from utils.db_api.database import create_db
from utils.db_api.db_commands import add_item


async def add_items():
    await add_item(
        name='Iphone 13 mini', category_name='Гаджеты', category_code='Gadgets',
        subcategory_name='Iphones', subcategory_code='Phones', price=60000, photo='-'
    )
    await add_item(
        name='Iphone 13', category_name='Гаджеты', category_code='Gadgets',
        subcategory_name='Iphones', subcategory_code='Phones', price=70000, photo='-'
    )
    await add_item(
        name='Iphone 13 pro', category_name='Гаджеты', category_code='Gadgets',
        subcategory_name='Iphones', subcategory_code='Phones', price=85000, photo='-'
    )
    await add_item(
        name='Iphone 13 pro max', category_name='Гаджеты', category_code='Gadgets',
        subcategory_name='Iphones', subcategory_code='Phones', price=90000, photo='-'
    )
    await add_item(
        name='Ipad mini', category_name='Гаджеты', category_code='Gadgets',
        subcategory_name='Ipads', subcategory_code='Pads', price=40000, photo='-'
    )
    await add_item(
        name='Ipad', category_name='Гаджеты', category_code='Gadgets',
        subcategory_name='Ipads', subcategory_code='Pads', price=50000, photo='-'

    )
    await add_item(
        name='Macbook Pro M2', category_name='Ноутбуки', category_code='Notes',
        subcategory_name='Macbook Pro', subcategory_code='Pro', price=140000, photo='-'
    )
    await add_item(
        name='Macbook Air M1', category_name='Ноутбуки', category_code='Notes',
        subcategory_name='Macbook Air', subcategory_code='Air', price=95000, photo='-'

    )
    await add_item(
        name='Macbook Pro M1max', category_name='Ноутбуки', category_code='Notes',
        subcategory_name='Macbook Pro', subcategory_code='Pro', price=140000, photo='-'
    )
    await add_item(
        name='Macbook Air M2', category_name='Ноутбуки', category_code='Notes',
        subcategory_name='Macbook Air', subcategory_code='Air', price=125000, photo='-'

    )


# loop = asyncio.get_event_loop()
# loop.run_until_complete(create_db())
# loop.run_until_complete(add_items())
