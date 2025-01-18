import os
from dotenv import load_dotenv
import telebot
from telebot.types import BotCommand
from musics_ans import music
import time
from random import choice, shuffle

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(token=TOKEN)
commands = [BotCommand('/game','начать игру')]
bot.set_my_commands(commands)

users = {}


def generate_markup(right_answer, wrong_answers):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) #создаем тг клавиатуру 
    answers = wrong_answers + [right_answer] #комбинируем правиьные и неправильные ответы 
    shuffle(answers) #перемещиваем все ответы 
    for item in answers:
        markup.add(item)#добавляем каждый ответ 
    return markup #возращаем готовую клавиатуру


@bot.message_handler(commands=["game"])
def game(message):
    song = choice(music)#выбираем элемент в списке 
    markup = generate_markup(song['right'], song['wrong'])#добавляем наши ответы основываясь на случайном выборе
    bot.send_voice(message.chat.id, song['id'], reply_markup=markup)#Отправляем песню по ее айди
    users[message.chat.id] = song['right']


@bot.message_handler(content_types=['text'])
def check_answers(message):
    right = users.get(message.chat.id, None) # получаем правильный ответ 
    #условия
    if not right:
        bot.send_message(message.chat.id, "Чтобы начать игру выберите команду /game")
        return None
    if message.text == right:
        text = "Верно"
    else: 
        text = "вы не угадали , увы"

    bot.send_message(message.chat.id, text, reply_markup=telebot.types.ReplyKeyboardRemove())
    users.pop(message.chat.id)
    bot.send_message(message.chat.id, text='Если хотите сыграть еше , выберете команду /game')

bot.infinity_polling()