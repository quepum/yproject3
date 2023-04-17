import base64
import sqlite3
from pathlib import Path

import telebot
import requests
from telebot import types  # для указание типов
from config import BOT_TOKEN
from text import rules, rules2, text_picture1, text_picture2, text_picture3


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Начать игру")
    button2 = types.KeyboardButton("Есть вопросик")
    button3 = types.KeyboardButton("Узнать правила игры")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот-помощник для проекта фото-квеста 'Назад в прошлое'".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Начать игру"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Задание 1")
        button2 = types.KeyboardButton("Задание 2")
        button3 = types.KeyboardButton("Задание 3")
        home = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, button2, button3, home)
        bot.send_message(message.chat.id,
                         text='\n'.join(rules), reply_markup=markup)
    elif (message.text == "Узнать правила игры"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Начать игру")
        home = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, home)
        bot.send_message(message.chat.id,
                         text='\n'.join(rules2), reply_markup=markup)

    elif (message.text == "Есть вопросик"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Начать игру")
        home = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1, home)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    # в этих трех условиях бот отправляет человеку фоточки заданий с их текстом
    elif (message.text == "Задание 1"):
        img = open('pictures/first_picture.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, text='\n'.join(text_picture1))

    elif (message.text == "Задание 2"):
        img = open('pictures/second_picture.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, text='\n'.join(text_picture2))

    elif (message.text == "Задание 3"):
        img = open('pictures/third_picture.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, text='\n'.join(text_picture3))

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Начать игру")
        button2 = types.KeyboardButton("Есть вопросик")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         text="К сожалению, такой команды я не знаю. Может ты имел ввиду что-то другое?")


@bot.message_handler(content_types=['photo'])
def save_photo(message):
    print('tyjtyj')
    Path(f'files/{message.chat.id}/photos').mkdir(parents=True, exist_ok=True)

    try:
        # сохраним изображение
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'files/{message.chat.id}/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        with open(src, "rb") as image_file:
            encoded_string = sqlite3.Binary(image_file.read())

        # откроем БД и запишем информацию (ID пользователя, фото)
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Pictures VALUES (?, ?)', (message.chat.id, encoded_string))
        conn.commit()
        bot.reply_to(message, "Очень классно получилось!)")

    except Exception as e:
        bot.reply_to(message, e)


bot.polling(none_stop=True)
