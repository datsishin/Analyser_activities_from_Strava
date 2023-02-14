import telebot
import os
from dotenv import load_dotenv
from json_worker import generation_analyse

load_dotenv()

token = os.getenv('TELEGRAM_API_TOKEN')

bot = telebot.TeleBot(token)

# choise_the_training = {'the_last': 0,
#                        'the_second': 1}


@bot.message_handler(commands=['start'])
def start_message(message):
    text = f'<b>Hello, {message.from_user.username}</b>'
    bot.send_message(message.chat.id, text=text, parse_mode='html')


@bot.message_handler(commands=['last_training'])
def get_statistics(message):
    text = generation_analyse()
    bot.send_message(message.chat.id, text=text)


bot.polling(none_stop=True)
if __name__ == '__main__':
    get_statistics()
