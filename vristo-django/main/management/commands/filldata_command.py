from django.core.management.base import BaseCommand
from main.factories import CDNFactory, DomainFactory, HostingCategoryFactory, HostingFactory, \
    ServiceProviderFactory, WebsiteCategoryFactory, WebsiteFactory


class Command(BaseCommand):
    help = 'Create Fake Date'

    def handle(self, *args, **kwargs):
        for _ in range(10):
            ServiceProviderFactory()

        for _ in range(10):
            DomainFactory()

        for _ in range(2):
            HostingCategoryFactory()

        for _ in range(5):
            HostingFactory()

        for _ in range(5):
            CDNFactory()

        for _ in range(2):
            WebsiteCategoryFactory()

        for _ in range(10):
            WebsiteFactory()

        self.stdout.write(self.style.SUCCESS('Complete'))
