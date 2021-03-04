from django.contrib import admin
from .models import User, Account, Transaction

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "first_name",
        "last_name",
        "email_id",
        "is_active",
        "created_at",
        "updated_at",
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "account_number",
        "amount",
        "user",
        "is_active",
        "created_at",
        "updated_at",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "account",
        "amount",
        "operation",
        "transaction_date",
        "is_active",
        "created_at",
        "updated_at",
    )
