from django.db import models

from django_project.telegrambot.core.models import TimeBasedModel


class User(TimeBasedModel):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(
        unique=True,
        verbose_name='ID пользователя телеграм'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя'
    )
    username = models.CharField(
        max_length=50,
        verbose_name='Username телеграм'
    )
    email = models.EmailField(
        max_length=60,
        verbose_name='Email'
    )

    def __str__(self):
        return f'{self.id} ({self.user_id}) - {self.name}'

# class Referral(TimeBasedModel):
#     class Meta:
#         verbose_name = 'Реферал'
#         verbose_name_plural = 'Рефералы'
#
#     id = models.OneToOneField(
#         User,
#         unique=True,
#         primary_key=True,
#         on_delete=models.CASCADE
#     )
#     referrer_id = models.BigIntegerField()
#
#     def __str__(self):
#         return f'№ {self.id} - от {self.referrer_id}'
