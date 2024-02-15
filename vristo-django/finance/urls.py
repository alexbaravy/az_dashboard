from django.urls import path
from . import views

urlpatterns = [
    path('finance/transaction_table', views.transaction_table, name='transaction_table'),
    path('finance/diagrams', views.diagrams, name='diagrams'),
]