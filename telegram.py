import telebot
import os
from dotenv import load_dotenv

from json_worker import generation_analyse, get_stat
from main import get_mileage_for_service

load_dotenv()

token = os.getenv('TELEGRAM_API_TOKEN')

bot = telebot.TeleBot(token)
nl = '\n'


@bot.message_handler(commands=['start'])
def say_hi(message):
    text = 'Hi!'
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['get_last_training'])
def get_training_data(message):
    text = generation_analyse()
    bot.send_message(message.chat.id, text=text)
    bot.send_photo(message.chat.id, photo=open('picture.png', 'rb'))
    bot.send_photo(message.chat.id, photo=open('graph.png', 'rb'))


@bot.message_handler(commands=['time_statistics'])
def get_statistics(message):
    data = get_stat()
    bot.send_message(message.chat.id, text=f'Время тренировок за последние 7 дней:{nl}{data[0]}'
                                           f'{nl}'
                                           f'{nl}'
                                           f'Время тренировок за последние 30 дней:{nl}{data[1]}')


@bot.message_handler(commands=['service'])
def get_service_info(message):
    text = get_mileage_for_service()
    bot.send_message(message.chat.id, text=text)


bot.polling(none_stop=True)
