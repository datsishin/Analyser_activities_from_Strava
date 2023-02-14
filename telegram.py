import telebot
import os
from dotenv import load_dotenv
from json_worker import generation_analyse, get_stat

# from total_time_statistics import get_stat

load_dotenv()

token = os.getenv('TELEGRAM_API_TOKEN')

bot = telebot.TeleBot(token)
nl = '\n'


@bot.message_handler(commands=['last_training'])
def get_training_data(message):
    text = generation_analyse()
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['stat'])
def get_statistics(message):
    week_time = get_stat()[0]
    month_time = get_stat()[1]
    bot.send_message(message.chat.id, text=f'Время тренировок за последние 7 дней:{nl}{week_time}'
                                           f'{nl}'
                                           f'{nl}'
                                           f'Время тренировок за последние 30 дней:{nl}{month_time}')


bot.polling(none_stop=True)
if __name__ == '__main__':
    get_training_data()
    get_statistics()
