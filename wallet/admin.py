from django.contrib import admin
from .models import Transaction, Notification, Product, Order, Advertisement

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'amount', 'status', 'created_at']
    list_filter = ['type', 'status']
    search_fields = ['user__email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_active']
    list_filter = ['is_active', 'category']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'total_amount', 'status', 'created_at']

admin.site.register(Notification)
admin.site.register(Advertisement)
