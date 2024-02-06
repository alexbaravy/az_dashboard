from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import CDN, Hosting, Domain, Website
from .utils import ExpirationNotifier, TelegramNotifier, WebsiteChecker
import os

notifier = TelegramNotifier(token=os.environ.get('BOT_TOKEN'), chat_id=os.environ.get('CHAT_ID'))

@shared_task
def get_websites():
    checker = WebsiteChecker(notifier=notifier, az_verification_tag=os.environ.get('AZ_VERIFICATION_TAG'))

    websites = Website.objects.filter(
        check_enabled=True,
        deactivated=False
    ).values('id', 'domain__url', 'domain_hash')

    for website in websites:
        checker.check_website(website['id'], website['domain__url'], website['domain_hash'])


@shared_task
def get_expiration_services():
    expiration_notifier = ExpirationNotifier(notifier=notifier)

    now = timezone.now()
    days_later = now + timezone.timedelta(days=10)

    services_to_check = [
        (Domain, 'url'),
        (Hosting, 'ip'),
        (CDN, 'ip')
    ]

    for model, field_name in services_to_check:
        expiration_notifier.check_services(model, field_name, days_later)
