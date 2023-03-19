from django.contrib import admin

from .models import User  # ,Referral


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'name', 'username', 'created_at')


# @admin.register(Referral)
# class ReferralAdmin(admin.ModelAdmin):
#     list_display = ('id', 'referrer_id')
