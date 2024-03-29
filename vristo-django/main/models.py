import hashlib
from django.db import models
from django.utils import timezone


# Create your models here.
class ModelMetaClass(type(models.Model)):
    def get_verbose_name_plural(cls):
        return cls._meta.verbose_name_plural


class BaseCredential(models.Model):
    login = models.CharField(max_length=50, default='admin')
    password = models.CharField(max_length=255, default='admin')

    class Meta:
        abstract = True


class ServiceProvider(BaseCredential):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    note = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class BaseService(models.Model, metaclass=ModelMetaClass):
    service_provider = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    check_enabled = models.BooleanField(default=True)
    deactivated = models.BooleanField(default=False)
    note = models.TextField(max_length=255, blank=True)

    class Meta:
        abstract = True

    select_related_fields = ['service_provider']


class Domain(BaseService):
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = 'Domains'

    display_fields = ['id', 'service_provider__name', 'url', 'start_date', 'end_date', 'note']


class HostingCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Hosting categories'


class Hosting(BaseService, BaseCredential):
    ip = models.GenericIPAddressField(verbose_name='IP')
    category = models.ForeignKey(HostingCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name_plural = 'Hostings'

    select_related_fields = ['service_provider', 'category']
    display_fields = ['id', 'service_provider__name', 'category__name', 'ip', 'start_date', 'end_date', 'note']


class CDN(BaseService, BaseCredential):
    ip = models.GenericIPAddressField(blank=False, null=False)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'CDN'
        verbose_name_plural = 'CDN Providers'

    display_fields = ['id', 'service_provider__name', 'ip', 'start_date', 'end_date', 'note']


class WebsiteCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Website categories'


class Website(models.Model, metaclass=ModelMetaClass):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(WebsiteCategory, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    domain_hash = models.CharField(max_length=128, blank=True, editable=False)
    hosting = models.ForeignKey(Hosting, on_delete=models.CASCADE)
    cdn = models.ForeignKey(CDN, on_delete=models.CASCADE, null=True, blank=True)
    check_enabled = models.BooleanField(default=True)
    deactivated = models.BooleanField(default=False)
    note = models.TextField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            domain_hash = hashlib.sha256(self.domain.url.encode('utf-8')).hexdigest()
            self.domain_hash = domain_hash
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Websites'

    select_related_fields = ['category', 'domain', 'hosting', 'cdn']
    display_fields = ['id', 'name', 'category__name', 'domain__url', 'hosting__ip', 'cdn__ip', 'note']


class UnavailableLog(models.Model, metaclass=ModelMetaClass):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    start_status = models.IntegerField(null=True, blank=True)
    end_status = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Unavailable Logs'

    select_related_fields = ['website']
    display_fields = ['id', 'website__name', 'start_date', 'end_date', 'start_status', 'end_status']