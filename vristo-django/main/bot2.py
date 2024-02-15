import logging
import telebot
from telebot import types
import requests
from typing import List, Dict
import os


class APIClient:
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url
        self.headers = {'Authorization': f'{api_token}'}

    def make_request(self, endpoint: str) -> str:
        try:
            response = requests.get(f"{self.api_url}{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return [str(e)]


class TableFormatter:
    @staticmethod
    def format(data_list: List[List[str]], headers: List[str]) -> str:
        column_widths = [len(header) for header in headers]
        for row in data_list:
            for i, cell in enumerate(row):
                column_widths[i] = max(column_widths[i], len(str(cell)))

        header_row = ' | '.join(header.ljust(column_widths[i]) for i, header in enumerate(headers))
        separator = '+'.join('-' * column_widths[i] for i, _ in enumerate(headers))
        data_rows = [' | '.join(str(cell).ljust(column_widths[i]) for i, cell in enumerate(row)) for row in data_list]

        return '\n'.join([header_row, separator] + data_rows)


class BotHandler:
    def __init__(self, bot_token: str, api_client: APIClient):
        self.bot = telebot.TeleBot(bot_token)
        self.api_client = api_client
        self.handlers = {
            'CDN Providers': self._handle_cdn_providers,
            'Domains': self._handle_domains,
            'Hostings': self._handle_hostings,
            'Websites': self._handle_websites,
            'Unavailable Logs': self._handle_unavailable_logs
        }

    def _handle_api_request(self, message: types.Message, endpoint: str, headers: List[str]):
        data = self.api_client.make_request(endpoint)
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            data_list = [[item.get(header, '') for header in headers] for item in data]
            formatted_table = TableFormatter.format(data_list, headers)
            self.bot.send_message(message.chat.id, text=f"{message.text}:\n" + formatted_table,
                                  disable_web_page_preview=True)
        else:
            self.bot.send_message(message.chat.id, text="No data available or error fetching data.")

    def _handle_cdn_providers(self, message: types.Message):
        headers = ['id', 'service_provider_name', 'ip', 'start_date', 'end_date', 'check_enabled', 'deactivated',
                   'note']
        self._handle_api_request(message, 'cdns', headers)

    def _handle_domains(self, message: types.Message):
        headers = ['id', 'service_provider_name', 'url', 'start_date', 'end_date', 'check_enabled', 'deactivated',
                   'note']
        self._handle_api_request(message, 'domains', headers)

    def _handle_hostings(self, message: types.Message):
        headers = ['id', 'service_provider_name', 'category_name', 'start_date', 'end_date', 'check_enabled',
                   'deactivated', 'note']
        self._handle_api_request(message, 'hostings', headers)

    def _handle_websites(self, message: types.Message):
        headers = ['id', 'service_provider_name', 'category_name', 'start_date', 'end_date', 'check_enabled',
                   'deactivated', 'note']
        self._handle_api_request(message, 'websites', headers)

    def _handle_unavailable_logs(self, message: types.Message):
        headers = ['id', 'domain_name', 'start_date', 'end_date', 'start_status', 'end_status']
        self._handle_api_request(message, 'unavailable-logs', headers)

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start(message: types.Message):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for button in self.handlers.keys():
                markup.add(types.KeyboardButton(button))
            self.bot.send_message(message.chat.id, "Hello! I'm your helper", reply_markup=markup)

        @self.bot.message_handler(content_types=['text'])
        def handle_text(message: types.Message):
            handler = self.handlers.get(message.text)
            if handler:
                handler(message)
            else:
                self.bot.send_message(message.chat.id, "I don't know this command")

        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    api_client = APIClient(api_url=os.environ.get('API_URL', 'http://127.0.0.1:8000/api/v1/'),
                           api_token=os.environ.get('API_TOKEN'))
    handler = BotHandler(bot_token=os.environ.get('BOT_TOKEN_FOR_API'), api_client=api_client)
    handler.run()
