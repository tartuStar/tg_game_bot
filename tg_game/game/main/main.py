import telebot

bot = telebot.TeleBot("8486071865:AAHEI1dUX63DUZIqx9PDde6wQBLDnbqhuyA")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()
# повертає те що ти йому написав (безжально спизжений код)
