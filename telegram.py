import glob
import logging
import time
import os

from dotenv import load_dotenv
from telebot import types
from telebot.types import InputMediaPhoto
import telebot

from db.service_of_bike import cleaning
from processors.json_worker import generation_analyse
from main import get_mileage
from processors.stats_graber import get_stats, get_full_stats, get_TSS_diagram, delete_all
from users import nl

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_API_TOKEN'))


def get_training_data(message):
    user_id = message.chat.id
    text = generation_analyse(user_id)
    bot.send_message(user_id, text=text)

    map_path = 'media/map.png'
    power_path = 'media/graph_by_power.png'
    hr_path = 'media/graph_by_hr.png'
    list_of_pic = []

    if os.path.exists(map_path):
        list_of_pic.append(InputMediaPhoto(open(map_path, 'rb')))
    if os.path.exists(power_path):
        list_of_pic.append(InputMediaPhoto(open(power_path, 'rb')))
    if os.path.exists(hr_path):
        list_of_pic.append(InputMediaPhoto(open(hr_path, 'rb')))

    bot.send_media_group(user_id, list_of_pic, disable_notification=True)

    files = glob.glob('media/*')
    for f in files:
        os.remove(f)


def get_statistics(message):
    user_id = message.chat.id
    data = get_stats(user_id)
    graph = get_TSS_diagram(user_id)

    if type(data) == list:
        bot.send_message(user_id, text=f'Время тренировок за последние 7 дней:{nl}{data[0]}'
                                       f'{nl}'
                                       f'{nl}'
                                       f'Время тренировок за последний 31 день:{nl}{data[1]}'
                                       f'{nl}'
                                       f'{nl}'
                                       f'Время тренировок за последние 365 дней:{nl}{data[2]}'
                                       f'{nl}'
                                       f'{nl}'
                                       f'Время тренировок за все время:{nl}{data[3]}'
                                       f'{nl}'
                                       f'{nl}'
                                       f'TSS за последние 7 дней (ATL): {data[4]}'
                                       f'{nl}'
                                       f'{nl}'
                                       f'TSS за последние 6 недель (CTL): {data[5]}'
                                       f'{nl}'
                                       f'{nl}'
                                       f'TSB: {data[6]}')

    if type(data) == str:
        bot.send_message(user_id, text=data)

    if graph == 'ok':
        bot.send_photo(user_id, photo=open('media/graph_by_TSS.png', 'rb'))

        files = glob.glob('media/*')
        for f in files:
            os.remove(f)


def get_service_info(message):
    user_id = message.chat.id
    text = get_mileage(user_id)
    bot.send_message(user_id, text=text)


def get_fully_stat(message, param: str = None):
    user_id = message.chat.id

    if param:
        delete_all(user_id)
        bot.send_message(user_id, text='Данные удалены')

    else:
        text = get_full_stats(user_id)
        bot.send_message(user_id, text=text)


def service(message, param: str):
    user_id = message.chat.id
    text = cleaning(message, param)
    bot.send_message(user_id, text, reply_markup=service_keyboard())


@bot.message_handler(commands=['start'])
def start(message):
    text = f'Привет, {message.chat.first_name}!{nl}' \
           f'Выбери интересующий пункт меню ⬇'
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Последняя тренировка')
    item2 = types.KeyboardButton('Статистика')
    item3 = types.KeyboardButton('Загрузить тренировки')
    item4 = types.KeyboardButton('Пробег')
    item5 = types.KeyboardButton('Обслуживание')
    item6 = types.KeyboardButton('Удалить данные')

    markup.add(item1, item2, item3, item4, item5, item6)
    return markup


def service_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Почистил цепь')
    item2 = types.KeyboardButton('Почистил привод')
    item3 = types.KeyboardButton('Последнее обслуживание')
    item4 = types.KeyboardButton('Выход')

    markup.add(item1, item2, item3, item4)
    return markup


def confirmation_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Да')
    item2 = types.KeyboardButton('Нет')

    markup.add(item1, item2)
    return markup


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Последняя тренировка':
            get_training_data(message)

        if message.text == 'Статистика':
            get_statistics(message)

        if message.text == 'Пробег':
            get_service_info(message)

        if message.text == 'Загрузить тренировки':
            get_fully_stat(message)

        if message.text == 'Обслуживание':
            chat_id = message.chat.id
            text = f'Выбери интересующий пункт меню ⬇'
            bot.send_message(chat_id, text, reply_markup=service_keyboard())

        if message.text == 'Почистил цепь':
            service(message, param='chain')

        if message.text == 'Почистил привод':
            service(message, param='drive')

        if message.text == 'Последнее обслуживание':
            service(message, param='info')

        if message.text in ('Выход', 'Нет'):
            chat_id = message.chat.id
            text = f'Выбери интересующий пункт меню ⬇'
            bot.send_message(chat_id, text, reply_markup=main_keyboard())

        if message.text == 'Удалить данные':
            chat_id = message.chat.id
            text = f'Уверен?'
            bot.send_message(chat_id, text, reply_markup=confirmation_keyboard())

        if message.text == 'Да':
            chat_id = message.chat.id
            get_fully_stat(message, param='delete')
            text = f'Выбери интересующий пункт меню ⬇'
            bot.send_message(chat_id, text, reply_markup=main_keyboard())


while True:
    try:
        logging.info("Bot running")
        bot.polling(none_stop=True, timeout=10)
        break
    except telebot.apihelper.ApiException as ex:
        logging.error(ex)
        bot.stop_polling()

        time.sleep(1)

        logging.info("Running again!")
