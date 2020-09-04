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
class OrderAdmin(admin.ModelAdmin):
    fields = ['timestamp', 'seat_number', ('status', 'status_changed'), ('payment_method', 'payment_amount'), 'total_price']
    readonly_fields = ['timestamp', 'status_changed', 'total_price']

    inlines = [OrderItemInlineAdmin]
