

from django_project.telegrambot.manage_users.models import User
from django_project.telegrambot.items.models import Item

from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id: int):
    user = User.objects.get(user_id=user_id)
    return user


@sync_to_async
def add_user(user_id, full_name, username):
    try:
        return User(user_id=int(user_id), name=full_name, username=username).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def select_all_users():
    users = User.objects.all()
    return users


@sync_to_async
def count_users():
    return User.objects.count()


@sync_to_async
def add_item(**kwargs):
    new_item = Item(**kwargs).save()
    return new_item


@sync_to_async
def get_categories() -> list[Item]:
    return Item.objects.distinct('category_name').all()


@sync_to_async
def get_subcategories(category_code) -> list[Item]:
    return Item.objects.distinct('subcategory_name').filter(category_code=category_code).all()


@sync_to_async
def count_items(category_code, subcategory_code=None) -> int:
    conditions = dict(category_code=category_code)
    if subcategory_code:
        conditions.update(subcategory_code=subcategory_code)
    return Item.objects.filter(**conditions).count()


@sync_to_async
def get_items(category_code, subcategory_code) -> list[Item]:
    return Item.objects.filter(category_code=category_code, subcategory_code=subcategory_code).all()


@sync_to_async
def get_item(item_id) -> Item:
    return Item.objects.get(id=int(item_id))





