import hashlib
import factory
from faker import Faker
from .models import ServiceProvider, Domain, Hosting, CDN, Website, UnavailableLog, HostingCategory, WebsiteCategory
import random

fake = Faker()


class ServiceProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServiceProvider

    name = factory.LazyAttribute(lambda _: fake.company())
    url = factory.LazyAttribute(lambda _: fake.url())


class DomainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Domain

    url = factory.LazyAttribute(lambda _: fake.url())
    service_provider = factory.LazyAttribute(lambda o: random.choice(ServiceProvider.objects.all()))
    start_date = factory.LazyAttribute(lambda _: fake.date_this_decade())
    end_date = factory.LazyAttribute(lambda _: fake.date_this_decade())
    check_enabled = factory.Faker('boolean', chance_of_getting_true=50)
    deactivated = factory.Faker('boolean', chance_of_getting_true=50)

class HostingCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HostingCategory

    name = factory.LazyAttribute(lambda _: fake.word())

class HostingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hosting

    ip = factory.LazyAttribute(lambda _: fake.ipv4())
    category = factory.LazyAttribute(lambda o: random.choice(HostingCategory.objects.all()))
    service_provider = factory.LazyAttribute(lambda o: random.choice(ServiceProvider.objects.all()))
    start_date = factory.LazyAttribute(lambda _: fake.date_this_decade())
    end_date = factory.LazyAttribute(lambda _: fake.date_this_decade())
    login = factory.LazyAttribute(lambda _: fake.user_name())
    password = factory.LazyAttribute(lambda _: fake.password())
    check_enabled = factory.Faker('boolean', chance_of_getting_true=50)
    deactivated = factory.Faker('boolean', chance_of_getting_true=50)


class CDNFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CDN

    ip = factory.LazyAttribute(lambda _: fake.ipv4())
    service_provider = factory.LazyAttribute(lambda o: random.choice(ServiceProvider.objects.all()))
    start_date = factory.LazyAttribute(lambda _: fake.date_this_decade())
    end_date = factory.LazyAttribute(lambda _: fake.date_this_decade())
    login = factory.LazyAttribute(lambda _: fake.user_name())
    password = factory.LazyAttribute(lambda _: fake.password())
    check_enabled = factory.Faker('boolean', chance_of_getting_true=50)
    deactivated = factory.Faker('boolean', chance_of_getting_true=50)


class WebsiteCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WebsiteCategory

    name = factory.LazyAttribute(lambda _: fake.word())


class WebsiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Website

    name = factory.LazyAttribute(lambda _: fake.company())
    category = factory.LazyAttribute(lambda o: random.choice(WebsiteCategory.objects.all()))
    domain = factory.LazyAttribute(lambda o: random.choice(Domain.objects.all()))
    hosting = factory.LazyAttribute(lambda o: random.choice(Hosting.objects.all()))
    cdn = factory.LazyAttribute(lambda o: random.choice(CDN.objects.all()))
    check_enabled = factory.Faker('boolean', chance_of_getting_true=100)
    deactivated = factory.Faker('boolean', chance_of_getting_true=0)

    @factory.post_generation
    def set_domain_hash(self, create, extracted, **kwargs):
        if create:
            domain_hash = hashlib.sha256(self.domain.url.encode('utf-8')).hexdigest()
            self.domain_hash = domain_hash