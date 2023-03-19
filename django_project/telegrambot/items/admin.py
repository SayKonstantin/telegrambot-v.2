from django.contrib import admin

from .models import Item, Purchase


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category_name', 'subcategory_name')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'item_id', 'quantity', 'receiver', 'created_at', 'successful')
