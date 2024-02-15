import factory
from faker import Faker
from .models import Currency, Account, Category, Transaction
import random

fake = Faker()

class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency

    name = factory.LazyAttribute(lambda _: fake.currency_name())
    symbol = factory.LazyAttribute(lambda _: fake.currency_symbol())


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    name = factory.LazyAttribute(lambda _: fake.company())
    balance = factory.LazyAttribute(lambda _: fake.random_number(digits=6))
    currency = factory.LazyAttribute(lambda _: random.choice(Currency.objects.all()))


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: fake.word())
    type = factory.LazyFunction(lambda: random.choice(['income', 'expense']))


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    account = factory.LazyAttribute(lambda _: random.choice(Account.objects.all()))
    category = factory.LazyAttribute(lambda _: random.choice(Category.objects.all()))
    amount = factory.LazyAttribute(lambda _: fake.random_number(digits=3))
    description = factory.LazyAttribute(lambda _: fake.text())
    date = factory.LazyAttribute(lambda _: fake.date_this_decade())
    type = factory.LazyFunction(lambda: random.choice(['income', 'expense']))

    @factory.post_generation
    def update_account_balance(self, create, extracted, **kwargs):
        if create:
            if self.type == 'income':
                self.account.balance += self.amount
            elif self.type == 'expense':
                self.account.balance -= self.amount
            self.account.save()