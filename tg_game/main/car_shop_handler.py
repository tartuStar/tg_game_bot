import sqlite3
import telebot
from telebot import types #Для кнопочок
from main import bot

def show_car_page(chat_id, page_num):
    conn = sqlite3.connect("main_DB.sqlite3")
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    item_per_page = 10
    offset = item_per_page * page_num

    c.execute("SELECT * FROM cars LIMIT ? OFFSET ?", (item_per_page, offset))
    cars = c.fetchall()

    markup = types.InlineKeyboardMarkup()

    for car_id, name, price in cars:
        btn = types.InlineKeyboardButton(text=f"{name} - {price}", callback_data=f"buy_car_{car_id}")
        markup.add(btn)

        c.execute("SELECT COUNT(*) FROM cars")
        total = c.fetchone()[0]
        conn.close()    

    nav_buttons = []
    if page_num > 0:
        nav_buttons.append(types.InlineKeyboardButton("◀ Назад", callback_data=f"cars_page_{page_num - 1}"))
    if offset + item_per_page < total:
        nav_buttons.append(types.InlineKeyboardButton("Далі ▶", callback_data=f"cars_page_{page_num + 1}"))

    if nav_buttons:
        markup.row(*nav_buttons)

    bot.send_message(chat_id, f"Сторінка {page_num + 1}", reply_markup=markup)

def handle_car_page(call):
    page_num = int(call.data.split("_")[-1])
    bot.answer_callback_query(call.id)

    # замість нового повідомлення — редагуємо
    try:
        bot.edit_message_text(
            f"Сторінка {page_num + 1}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=build_car_page_markup(page_num)
        )
    except Exception:
        # fallback якщо не вдалося редагувати
        show_car_page(call.message.chat.id, page_num)
