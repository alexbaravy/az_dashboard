from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import CDN, Hosting, Domain, Website
from .utils import send_notification, check_website, notify_services
from django.contrib.auth.models import User



@shared_task
def get_websites():
    websites = Website.objects.filter(
        check_enabled=True,
        deactivated=False
    ).values('domain__url', 'domain_hash')

    for website in websites:
        check_website(website['domain__url'], website['domain_hash'])


@shared_task
def get_expiration_services():
    now = timezone.now()
    days_later = now + timezone.timedelta(days=10)

    domain_services = Domain.objects.filter(end_date__lt=days_later, check_enabled=True,
                                            deactivated=False).values('url', 'end_date')
    notify_services(domain_services, 'Domain')

    hosting_services = Hosting.objects.filter(end_date__lt=days_later, check_enabled=True,
                                              deactivated=False).values('ip', 'end_date')
    notify_services(hosting_services, 'Hosting')

    cdn_services = CDN.objects.filter(end_date__lt=days_later, check_enabled=True,
                                      deactivated=False).values('ip', 'end_date')
    notify_services(cdn_services, 'CDN')

