import telebot
from telebot import types
import sqlite3
import os
import requests

TOKEN = "8794061789:AAGKAt9yxIdTIH-YL1IyCXbp3fX_ZplrBz4"
bot = telebot.TeleBot(TOKEN)

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# إنشاء الجدول إن لم يكن موجوداً
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
''')
conn.commit()

def check_subscription(user_id):
    return True

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    btn_download = types.InlineKeyboardButton('📥 تحميل فيديو', callback_data='download_menu')
    btn_invite = types.InlineKeyboardButton('🔗 دعوة أصدقاء', callback_data='menu_invite')
    markup.add(btn_download)
    markup.add(btn_invite)
    
    bot.send_message(chat_id, "أهلاً بك في القائمة الرئيسية لبوت Ayoub Hub:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'main_menu':
        show_main_menu(call.message.chat.id)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
    elif call.data == 'menu_invite':
        user_id = call.from_user.id
        bot_info = bot.get_me()
        invite_link = f'https://t.me/{bot_info.username}?start={user_id}'
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('⬅️ القائمة الرئيسية', callback_data='main_menu'))
        
        text = f"مرحباً بك في قسم دعوة الأصدقاء!\n\n`{invite_link}`\n\nشارك الرابط مع أصدقائك."
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text and ('http://' in message.text or 'https://' in message.text))
def download_video(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, 'عليك الاشتراكات أولاً لاستخدام البوت.')
        return
        
    url = message.text.strip()
    msg = bot.reply_to(message, '⏳ جاري معالجة وتحميل المحتوى ...')
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
    }
    
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
            
        bot.delete_message(message.chat.id, msg.message_id)
        os.remove(filename)
    except Exception as e:
        bot.edit_message_text(f'حدث خطأ أثناء التحميل: {str(e)}', message.chat.id, msg.message_id)

bot.infinity_polling()
