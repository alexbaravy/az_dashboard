from django.db import models


class ModelMetaClass(type(models.Model)):
    def get_verbose_name_plural(cls):
        return cls._meta.verbose_name_plural


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Currencies'


class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=19, decimal_places=4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    name = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Transaction(models.Model, metaclass=ModelMetaClass):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    description = models.TextField(blank=True)
    date = models.DateField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.description} on {self.date}"

    class Meta:
        verbose_name_plural = 'Transactions'

    select_related_fields = ['account', 'category']
    display_fields = ['id', 'category__name', 'type', 'amount', 'date', 'description']
