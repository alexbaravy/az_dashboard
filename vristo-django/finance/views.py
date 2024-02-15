from django.shortcuts import render
from .models import Currency, Account, Category, Transaction
from django.db.models import Sum
from datetime import datetime


# Create your views here.
def get_model_data(model, headers):
    model_name = model.get_verbose_name_plural()
    data = model.objects.select_related(*model.select_related_fields).values(*model.display_fields).order_by('-date')
    return model_name, headers, data


def transaction_table(request):
    headers = ['ID', 'Category', 'Type', 'Amount', 'Date', 'Description']
    model_name, headers, transaction_data = get_model_data(Transaction, headers)

    for transaction in transaction_data:
        transaction['amount_style'] = 'color: green;'
        if transaction['type'] == 'expense':
            transaction['amount'] = f"-{transaction['amount']}"
            transaction['amount_style'] = 'color: red;'

    return render(request, 'finance/transaction_table.html',
                  {'model_name': model_name, 'headers': headers, 'transaction_data': transaction_data})


def diagrams(request):
    total_amount = Transaction.objects.values('type').annotate(total_amount=Sum('amount'))

    total_amount_new = {}
    for item in total_amount:
        if item['type'] == 'expense':
            total_amount_new['expense'] = round(item['total_amount'], 2)

        if item['type'] == 'income':
            total_amount_new['income'] = round(item['total_amount'], 2)


    return render(request, 'finance/diagrams.html',
                  {'total_amount': total_amount_new})
