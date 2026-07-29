from django.contrib import admin

from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_available', 'is_staff')
    list_filter = ('role', 'is_available', 'is_staff')
    search_fields = ('username', 'email', 'phone')