from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'get_full_name', 'account_status', 'balance', 'created_at']
    list_filter = ['account_status', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Wallet Info', {'fields': ('phone', 'account_number', 'balance', 'upi_id', 'account_status', 'account_opened', 'admin_note')}),
        ('KYC', {'fields': ('id_photo', 'profile_photo', 'address', 'city', 'state', 'pincode')}),
    )
