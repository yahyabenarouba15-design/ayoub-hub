import telebot

TOKEN = "8794061789:AAGKAt9yxIdTIH-YL1lyCXbp3fX_ZplrBz4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا يحيى! البوت يعمل الآن بنجاح تامة.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
