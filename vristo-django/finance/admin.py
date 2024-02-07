from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from .models import Account, Category, Currency, Transaction


class FinanceAdminSite(AdminSite):
    site_header = "AZ Dashboard2"
    site_title = "Finance Panel"
    index_title = "Finance Panel"

    def get_app_list(self, request):
        ordering = {
            'Accounts': 1,
            'Categories': 2,
            'Currencies': 3,
            'Transactions': 4
        }

        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list


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


finance_admin_site = FinanceAdminSite(name='finance_admin')

finance_admin_site.register(Account, AccountAdmin)
finance_admin_site.register(Category, CategoryAdmin)
finance_admin_site.register(Currency, CurrencyAdmin)
finance_admin_site.register(Transaction, TransactionAdmin)
