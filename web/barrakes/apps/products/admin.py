from django.contrib import admin
from django.conf import settings

from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'formatted_price', 'active']
    list_select_related = ['category']
    list_filter = ['category', 'active']
    search_fields = ['name']
    fields = ['name', 'category', 'price', 'active']
    autocomplete_fields = ['category']

    def formatted_price(self, obj):
        return '{} {}'.format(obj.price, settings.CURRENCY)
    formatted_price.short_description = 'price'
