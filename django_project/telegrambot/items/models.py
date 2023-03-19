from django.db import models

from django_project.telegrambot.core.models import TimeBasedModel
from django_project.telegrambot.manage_users.models import User


class Item(TimeBasedModel):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    image = models.ImageField('Изображение', upload_to='images')
    price = models.DecimalField(decimal_places=2, max_digits=8)
    description = models.TextField(max_length=1000)

    category_code = models.CharField(max_length=30)
    category_name = models.CharField(max_length=30)
    subcategory_code = models.CharField(max_length=30)
    subcategory_name = models.CharField(max_length=30)

    def __str__(self):
        return f'№ {self.id} - {self.name}'


class Purchase(TimeBasedModel):
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.SET(0), verbose_name='Покупатель')
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Идентификатор товара')
    amount = models.DecimalField(verbose_name='Стоимость', decimal_places=2, max_digits=8)
    quantity = models.IntegerField(verbose_name='Количество')
    purchase_time = models.DateTimeField(auto_now_add=True, verbose_name='Время покупки')
    shipping_address = models.JSONField(verbose_name='Адрес доставки', null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20)
    email = models.EmailField(max_length=50, null=True)
    receiver = models.CharField(verbose_name='Имя получателя', max_length=35)
    successful = models.BooleanField(verbose_name='Оплачено', default=False)

    def __str__(self):
        return f'№ {self.id} - {self.item_id} ({self.quantity})'
