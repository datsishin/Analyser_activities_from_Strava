import glob

from telebot.types import InputMediaPhoto
import telebot
import os
from dotenv import load_dotenv

from json_worker import generation_analyse, get_stat
from main import get_mileage_for_service

load_dotenv()

token = os.getenv('TELEGRAM_API_TOKEN')

first_user_id = os.getenv('FIRST_USR_ID')
second_user_id = os.getenv('SECOND_USER_ID')

bot = telebot.TeleBot(token)

nl = '\n'


@bot.message_handler(commands=['start'])
def say_hi(message):
    text = 'Hi!'
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['get_last_training'])
def get_training_data(message):
    user_id = message.chat.id
    text = generation_analyse(user_id)
    bot.send_message(user_id, text=text)
    # list_of_file = os.listdir('media')
    # count_of_picture = len([name for name in list_of_file if os.path.isfile(name)])
    #
    # for i in count_of_picture:
    #     with open(list_of_file[i], 'rb') as i
    #     i+=1
    #
    # bot.send_media_group(user_id, [InputMediaPhoto(i)], disable_notification=True)
    # InputMediaPhoto(f2)],
    # disable_notification=True)
    # with open('media/graph_by_power.png', 'rb') as f1: \
    # open('media/graph_by_hr.png', 'rb') as f2:
    # open('media/maps.png', 'rb') as f3:
    # bot.send_media_group(user_id, [InputMediaPhoto(f1)],
    # InputMediaPhoto(f2)],
    # disable_notification=True)
    # InputMediaPhoto(f3)],

    files = glob.glob('media/*')
    for f in files:
        os.remove(f)


@bot.message_handler(commands=['time_statistics'])
def get_statistics(message):
    user_id = message.chat.id
    data = get_stat()
    bot.send_message(user_id, text=f'Время тренировок за последние 7 дней:{nl}{data[0]}'
                                   f'{nl}'
                                   f'{nl}'
                                   f'Время тренировок за последние 30 дней:{nl}{data[1]}')


@bot.message_handler(commands=['service'])
def get_service_info(message):
    user_id = message.chat.id
    text = get_mileage_for_service()
    bot.send_message(user_id, text=text)


bot.polling(none_stop=True)
