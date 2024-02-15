from django.core.management.base import BaseCommand
from finance.factories import CurrencyFactory,AccountFactory,CategoryFactory,TransactionFactory


class Command(BaseCommand):
    help = 'Create Fake Date'

    def handle(self, *args, **kwargs):
        # CurrencyFactory()

        # AccountFactory()

        # for _ in range(10):
        #     CategoryFactory()

        for _ in range(1000):
            TransactionFactory()

        self.stdout.write(self.style.SUCCESS('Complete'))
