import requests
from celery import shared_task
from django.conf import settings
from time import sleep
from bs4 import BeautifulSoup
import telebot
from .models import Website, Domain

# telegram API keys
bot = telebot.TeleBot('6160113526:AAEpoXM_F43Fi9jMQ-1SUJ2ngFB-CtMNQKA')


@shared_task
def add():
    print(2)
    return 1 + 2


def check(url, domain_hash):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tag = soup.find('meta', {'name': 'az-verification'})

            if meta_tag and meta_tag.get('content') == domain_hash:
                response = f'{url}: OK'
                bot.send_message('-960606856', response)
                return "OK"
            else:
                response = f"{url}: Error: Не найден тег 'az-verification' или не совпадает значение хэша."
                bot.send_message('-960606856', response)
                return "Error: Не найден тег 'az-verification' или не совпадает значение хэша."
        else:
            response = f"{url}: Error: Ошибка HTTP {response.status_code}"
            bot.send_message('-960606856', response)
            return f"{url}: Error: Ошибка HTTP {response.status_code}"
    except requests.RequestException as e:
        response = f"{url}: Error: {str(e)}"
        bot.send_message('-960606856', response)
        return f"{url}: Error: {str(e)}"

@shared_task
def get_websites():
    websites = Website.objects.values('domain__url', 'domain_hash')
    for website in websites:
        check(website['domain__url'], website['domain_hash'])



