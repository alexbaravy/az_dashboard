from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from .models import Account, Category, Currency, Transaction


class AccountAdmin(admin.ModelAdmin):
    fields = ['name', 'balance', 'currency']
    list_display = ['name', 'balance', 'currency']
    search_fields = ['name', 'balance', 'currency']


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'parent_id', 'type']
    list_display = ['name', 'parent_id', 'type']
    search_fields = ['name', 'parent_id', 'type']


class CurrencyAdmin(admin.ModelAdmin):
    fields = ['name', 'symbol']
    list_display = ['name', 'symbol']
    search_fields = ['name', 'symbol']


class TransactionAdmin(admin.ModelAdmin):
    fields = ['account', 'category', 'amount', 'description', 'date', 'type']
    list_display = ['account', 'category', 'amount', 'description', 'date', 'type']
    search_fields = ['account', 'category', 'amount', 'description', 'date', 'type']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            account = obj.account
            if obj.type == 'income':
                account.balance += obj.amount
            elif obj.type == 'expense':
                account.balance -= obj.amount
            account.save()


admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Transaction, TransactionAdmin)
