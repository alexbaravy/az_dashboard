from typing import Optional
import telebot
import logging
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import Website, UnavailableLog
from django.db.models import QuerySet

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot = telebot.TeleBot(bot_token)
        self.chat_id = chat_id

    def send_notification(self, result: str):
        self.bot.send_message(self.chat_id, result, disable_web_page_preview=True)
        logger.info(f"Notification: {result}")


class WebsiteChecker:
    def __init__(self, notifier: TelegramNotifier, az_verification_tag: str):
        self.notifier = notifier
        self.az_verification_tag = az_verification_tag

    def check_website(self, id: int, url: str, domain_hash: str) -> Optional[str]:
        result = None
        response = None
        try:
            response = requests.get(url)
            if response.status_code == 200:
                result = self._process_successful_response(id, url, domain_hash, response)
            else:
                self._send_unavailable_log(id, response)
                result = f"{url}: Error: HTTP {response.status_code}"
        except requests.RequestException as e:
            result = f"{url}: Error: {str(e)}"
        finally:
            if result:
                self.notifier.send_notification(result)
            if response:
                self._send_unavailable_log(id, response)
            return result

    def _process_successful_response(self, id: int, url: str, domain_hash: str, response: requests.Response) -> str:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', {'name': self.az_verification_tag})
        website = Website.objects.get(id=id)
        latest_issue = website.unavailablelog_set.order_by('-id').first()
        if meta_tag and meta_tag.get('content') == domain_hash:
            if latest_issue and latest_issue.start_status != 200:
                return f'{url}: OK'
        else:
            response.status_code = 299
            return f"{url}: Error: Tag '{self.az_verification_tag}' not found or hash value does not match."

    def _send_unavailable_log(self, id: int, response: requests.Response):
        website = Website.objects.get(id=id)
        latest_issue = website.unavailablelog_set.order_by('-id').first()
        if latest_issue is None or (latest_issue.start_status != response.status_code):
            UnavailableLog.objects.filter(
                website_id=id,
                end_date=None
            ).update(
                end_date=timezone.now(),
                end_status=response.status_code
            )

            UnavailableLog.objects.create(
                website=website,
                end_date=None,
                start_status=response.status_code
            )


class ExpirationNotifier:
    def __init__(self, notifier: TelegramNotifier):
        self.notifier = notifier

    def check_services(self, model: type, field_name: str, end_date: timezone.datetime):
        services = model.objects.filter(
            end_date__lt=end_date,
            check_enabled=True,
            deactivated=False
        ).values(field_name, 'end_date')

        if isinstance(services, QuerySet) and services.exists():
            self.notify_expiration_services(services, model.__name__)

    def notify_expiration_services(self, services, service_name: str):
        for service in services:
            service_type = 'url' if 'url' in service else 'ip'
            result = f"{service_name}: {service[service_type]}. Expiration Date: {service['end_date']}"
            self.notifier.send_notification(result)
