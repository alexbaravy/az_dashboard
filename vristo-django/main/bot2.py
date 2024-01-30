import telebot
from telebot import types
import logging

bot = telebot.TeleBot('6737786334:AAGkEDiIt-24Qim7i8kYZyWS61-SWWRlEOM')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('CDN Providers')
    button2 = types.KeyboardButton('Domains')
    button3 = types.KeyboardButton('Hostings')
    button4 = types.KeyboardButton('Websites')
    button5 = types.KeyboardButton('Unavailable logs')
    markup.add(button1, button2, button3, button4, button5)

    bot.send_message(message.chat.id,
                     text="Hello, {0.first_name}! I'm your helper".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "CDN Providers":
        bot.send_message(message.chat.id, text="CDN Providers")
    elif message.text == "Domains":
        bot.send_message(message.chat.id, text="Domains")
    elif message.text == "Hostings":
        bot.send_message(message.chat.id, "Hostings")
    elif message.text == "Websites":
        bot.send_message(message.chat.id, text="Websites")
    elif message.text == "Unavailable logs":
        bot.send_message(message.chat.id, text="Unavailable logs")
    else:
        bot.send_message(message.chat.id, text="I dont know this command")


bot.polling(none_stop=True)
