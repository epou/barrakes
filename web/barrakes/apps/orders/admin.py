from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.


class OrderItemInlineAdmin(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity']
    readonly_fields = ['price', 'total_price']
    autocomplete_fields = ['product']
    extra = 0

@admin.register(Order)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = ['seat_number', ('status', 'status_changed'), 'total_price']
    readonly_fields = ['status_changed', 'total_price']

    inlines = [OrderItemInlineAdmin]
