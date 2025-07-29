# закоментовані бібліотеки не видаляти, вони треба будуть. Розкоментовувати по мірі необхідності

# conn.execute("PRAGMA foreign_keys = ON") вставляти після створення з'єднання з БД, обов'язково!!!!

#import random
import sqlite3
import telebot 
from telebot import types #Для кнопочок
import car_shop_handler

bot = telebot.TeleBot("8486071865:AAHEI1dUX63DUZIqx9PDde6wQBLDnbqhuyA")

def registration_handler(tg_id, username): # обробник реєстрації нових користувачів, якщо користувач є, то не запише, а скаже, що вже є такий
    conn = sqlite3.connect("main_DB.sqlite3") # ініціалізація БД
    c = conn.cursor() # створюємо курсор
    c.execute("INSERT OR IGNORE INTO User (tg_id, name) VALUES (?, ?)",(tg_id, username))
    if c.rowcount == 0:
        print("Такий запис вже існує") # тільки для відладки
        conn.commit()
    else:
        print("Новий запис додано") # тільки для відладки
        conn.commit()
        
@bot.message_handler(commands=["start"]) # commands=[""] реагує тільки на вручну написані команди типу "/start"
def game_start(message): # основний набір кнопок для швидкої навігації (бажано не рухати ніхуя)
    tg_id = message.from_user.id
    username = message.from_user.username or "anon"
    registration_handler(tg_id = tg_id, username = username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Магазин")
    btn2 = types.KeyboardButton("Статистика")
    btn3 = types.KeyboardButton("Землі")
    btn4 = types.KeyboardButton("Будівлі")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, "Що робимо?",reply_markup=markup)
    
"""
Потрібно подумати як організувати ці структури

@bot.message_handler(func=lambda msg: msg.text == "Статистика")
def stat_handler(message): 
	pass  

@bot.message_handler(func=lambda msg: msg.text == "Землі") 
def fields_handler(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Ліси", callback_data="forest_categori")
    btn2 = types.InlineKeyboardButton("Поля", callback_data = "field_categori")
    btn3 = types.InlineKeyboardButton("Озера", callback_data = "lakes_categori")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Що робимо?", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Будівлі")
def houses_handler(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Маєтки", callback_data="home_categori")
    btn2 = types.InlineKeyboardButton("Хліви", callback_data = "animal_home_categori")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Що робимо?", reply_markup=markup)

"""

@bot.message_handler(func=lambda msg: msg.text == "Магазин") # обробка з Keybord кнопок
def shop_handler(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Автомобілі", callback_data="car_categori")
    btn2 = types.InlineKeyboardButton("Поля", callback_data = "field_categori")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Що робимо?", reply_markup=markup)

"""
def car_sell_list(call): # обробка кнопочок Inline робиться через call в передаваному аргументі
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Audi 80 quattro", callback_data="buy_audi_80quattro")
    btn2 = types.InlineKeyboardButton("BMW X5", callback_data="buy_BMW_X5")
    markup.add(btn1, btn2)
    bot.send_message(call.message.chat.id, "Оберіть авто:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "car_categori") # для Inline кнопочок використовуєм декоратор callback_query_handler
def car_buyer_handler(call):
    markup = types.InlineKeyboardMarkup()

    conn = sqlite3.connect("main_DB.sqlite3")
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    c.execute("SELECT * FROM cars")
    cars_list = c.fetchall()

    for car in cars_list:
        car_id = car[0]
        car_name = car[1]
        car_price = car[2]
        car_btn = types.InlineKeyboardButton(text = f"{car_name} - {car_price}", callback_data = f"{car_id}")
        markup.add(car_btn)
    
    bot.send_message(call.message.chat.id, "Що робимо?",reply_markup=markup)
"""


bot.polling()
