import telebot
import logging
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import Website, UnavailableLog
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

# telegram API keys
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
chat_id = os.environ.get('CHAT_ID')

az_verification_tag = os.environ.get('AZ_VERIFICATION_TAG')


def send_notification(result):
    bot.send_message(chat_id, result, disable_web_page_preview=True)
    logger.info(f"Notification: {result}")


def send_unavailable_log(id, response):
    website = Website.objects.get(id=id)
    latest_issue = website.unavailablelog_set.order_by('-id').first()
    if latest_issue is None or (latest_issue.start_status != response.status_code):
        UnavailableLog.objects.filter(website_id=id, end_date=None).update(
            end_date=timezone.now(),
            end_status=response.status_code
        )

        UnavailableLog.objects.create(
            website=website,
            end_date=None,
            start_status=response.status_code
        )


def check_website(id, url, domain_hash):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tag = soup.find('meta', {'name': az_verification_tag})

            if meta_tag and meta_tag.get('content') == domain_hash:
                result = f'{url}: OK'
            else:
                result = f"{url}: Error: Tag 'az-verification' not found or hash value does not match."
                response.status_code = 299
        else:
            result = f"{url}: Error: HTTP {response.status_code}"

    except requests.RequestException as e:
        result = f"{url}: Error: {str(e)}"
    finally:
        send_notification(result)
        send_unavailable_log(id, response)
        return result


def notify_services(services, service_name):
    for service in services:
        service_type = 'url' if 'url' in service else 'ip'
        result = f"{service_name}: {service[service_type]}. Expiration Date: {service['end_date']}"
        send_notification(result)
        return result
