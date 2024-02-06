import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN_FOR_API'))
api_url = os.environ.get('API_URL')
api_token = os.environ.get('API_TOKEN')

headers = {'Authorization': f'Token {api_token}'}

handlers = {
    'CDN Providers': lambda message: handle_api_request(message, 'cdns',
                                                        ['id', 'service_provider_name', 'ip', 'start_date', 'end_date',
                                                         'check_enabled', 'deactivated', 'note']),
    'Domains': lambda message: handle_api_request(message, 'domains',
                                                  ['id', 'service_provider_name', 'url', 'start_date', 'end_date',
                                                   'check_enabled', 'deactivated',
                                                   'note']),
    'Hostings': lambda message: handle_api_request(message, 'hostings',
                                                   ['id', 'service_provider_name', 'category_name', 'start_date',
                                                    'end_date', 'check_enabled',
                                                    'deactivated', 'note']),
    'Websites': lambda message: handle_api_request(message, 'websites',
                                                   ['id', 'name', 'check_enabled', 'deactivated', 'note',
                                                    'category_name', 'domain_url',
                                                    'hosting_ip', 'cdn_ip']),
    'Unavailable logs': lambda message: handle_api_request(message, 'unavailable-log',
                                                           ['id', 'domain_name', 'start_date', 'end_date',
                                                            'start_status', 'end_status']),
}


def make_api_request(api_tail):
    try:
        response = requests.get(api_url + api_tail, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return str(e)


def format_as_table(data_list, headers):
    column_widths = [len(header) for header in headers]
    for row in data_list:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))

    header_row = ' | '.join(header.ljust(column_widths[i]) for i, header in enumerate(headers))
    separator = '+'.join('-' * column_widths[i] for i, _ in enumerate(headers))
    data_rows = []
    for row in data_list:
        data_row = ' | '.join(str(cell).ljust(column_widths[i]) for i, cell in enumerate(row))
        data_rows.append(data_row)

    table = [header_row, separator] + data_rows
    return '\n'.join(table)


def handle_api_request(message, api_tail, headers):
    data = make_api_request(api_tail)
    if isinstance(data, list) and len(data) > 0:
        data_list = [[item[header] for header in headers] for item in data]
        formatted_table = format_as_table(data_list, headers)
        bot.send_message(message.chat.id, text=f"{message.text}:\n" + formatted_table, disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, text="No data available or error fetching data.")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = list(handlers.keys())
    for button in buttons:
        markup.add(types.KeyboardButton(button))

    bot.send_message(message.chat.id,
                     text="Hello, {0.first_name}! I'm your helper".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    handler = handlers.get(message.text)
    if handler:
        handler(message)
    else:
        bot.send_message(message.chat.id, text="I dont know this command")


if __name__ == '__main__':
    bot.polling(none_stop=True)
