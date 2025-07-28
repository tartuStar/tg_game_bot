#закоментовані бібліотеки не видаляти, вони треба будуть. Розкоментовувати по мірі необхідності
#import random
import sqlite3
import telebot
from telebot import types #Для кнопочок


conn = sqlite3.connect("main_DB.sqlite3") # ініціалізація БД
c = conn.cursor() # створюємо курсор


bot = telebot.TeleBot("8486071865:AAHEI1dUX63DUZIqx9PDde6wQBLDnbqhuyA")

@bot.message_handler(commands=["start"]) # commands=[""] реагує тільки на вручну написані команди типу "/start"
def game_start(message): # основний набір кнопок для швидкої навігації (бажано не рухати ніхуя)
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
    
@bot.callback_query_handler(func=lambda call: call.data == "car_categori") # для Inline кнопочок використовуєм декоратор callback_query_handler
def car_sell_list(call): # обробка кнопочок Inline робиться через call в передаваному аргументі
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Audi", callback_data="buy_audi")
    btn2 = types.InlineKeyboardButton("BMW", callback_data="buy_BMW")
    markup.add(btn1, btn2)
    bot.send_message(call.message.chat.id, "Оберіть авто:", reply_markup=markup)
    
bot.polling()
