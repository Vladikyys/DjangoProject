from django.contrib import admin
from .models import Product, Genre, Cart, CartItem, Order
from mptt.admin import MPTTModelAdmin
# Register your models here.


class CategoryMPTTAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


admin.site.register(Product)
admin.site.register(Genre, CategoryMPTTAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)