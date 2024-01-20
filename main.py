import requests
import json
import telebot
from config import TOKEN, currency_dict, API_KEY
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message):
    bot_info = "Бот рассчитывает стоимость требуемой валюты.\n" \
               "Для работы с ботом используется введите запрос в формате:\n" \
               "<имя требуемой валюты> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.\n" \
               "Узнать список всех доступных валют: /values"
    bot.send_message(message.chat.id, bot_info)

@bot.message_handler(commands=['values'])
def get_values(message):
    values_info = "Список доступных валют:"
    for key in currency_dict.keys():
        values_info = "\n".join((values_info, key))
    bot.reply_to(message, values_info)

@bot.message_handler(content_types=['text'])
def converter(message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException("Некорректно введен запрос.")

        base, quote, amount = values

        base = base[0].upper() + base[1:]
        quote = quote[0].upper() + quote[1:]

        total_amount = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
    else:
        text = f'Стоимость {amount} "{base}" в "{quote}" равна {total_amount}'
        bot.send_message(message.chat.id, text)


print("Bot started")
bot.polling()
