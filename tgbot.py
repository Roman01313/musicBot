import os
from dotenv import load_dotenv
import telebot
from telebot.types import BotCommand
import time

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(token=TOKEN)
commands = [BotCommand('/music','отправить музыку')]
bot.set_my_commands(commands)

@bot.message_handler(content_types=['text'], commands=['music'])
def find_file_id(message):
    for file in os.listdir('music/'):
        if file.split('.')[-1] == 'ogg':
            f = open(f'music/{file}', 'rb')
            msg = bot.send_audio(message.chat.id, f , None)
            bot.send_message(message.chat.id, msg.voice.file_id)

bot.infinity_polling()