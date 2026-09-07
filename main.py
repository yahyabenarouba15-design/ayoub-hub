import os
import sqlite3
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
"""
)
conn.commit()


def check_subscription(user_id):
  return True


def show_main_menu(chat_id, message_id=None):
  text = (
      "🌟 *مـرحـبـاً بـك فـي عـالـم Ayoub Hub* 🌟\n\n"
      "┏━━━━ 🎯 *الـقـائـمـة الـرئـيـسـيـة* ━━━━┓\n"
      "┃ الإمبراطورية المتكاملة بين يديك الآن..\n"
      "┗━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
      "⚡ *اختر القسم الذي ترغب بالبدء فيه من الأزرار أدناه:*"
  )

  markup = types.InlineKeyboardMarkup(row_width=2)
  btn_download = types.InlineKeyboardButton(
      "📥 تحميل فيديو", callback_data="download_menu"
  )
  btn_turkish = types.InlineKeyboardButton(
      "🎬 المسلسلات التركية", callback_data="turkish_series"
  )
  btn_money = types.InlineKeyboardButton(
      "💳 كسب المال الذكي", callback_data="make_money"
  )
  btn_invite = types.InlineKeyboardButton(
      "🔗 دعوة الأصدقاء", callback_data="menu_invite"
  )

  markup.add(btn_download, btn_turkish, btn_money, btn_invite)

  if message_id:
    try:
      bot.edit_message_text(
          text,
          chat_id,
          message_id,
          reply_markup=markup,
          parse_mode="Markdown",
      )
    except:
      bot.send_message(
          chat_id, text, reply_markup=markup, parse_mode="Markdown"
      )
  else:
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id
  cursor.execute(
      "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
  )
  conn.commit()
  show_main_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
  if call.data == "main_menu":
    show_main_menu(call.message.chat.id, call.message.message_id)

  elif call.data == "download_menu":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = (
        "📥 *قـسـم تـحـمـيـل الـفـيـديـوهـات*\n\n"
        "أرسل أي رابط فيديو وسأقوم بتحميله لك فوراً بجودة عالية وسرعة خيالية! 🚀"
    )
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data == "turkish_series":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = (
        "🎬 *قـسـم الـمـسـلـسـلات الـتـركـيـة*\n\n"
        "🔥 استمتع بمشاهدة أحدث الحلقات والمسلسلات الحصرية بجودات خارقة.\n"
        "📌 *ترقبوا الإطلاقات الكبرى قريباً جداً!*"
    )
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data == "make_money":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = (
        "💳 *قـسـم كـسـب الـمـال بـدون بـطـاقـة هـويـة*\n\n"
        "💡 اكتشف الطرق الذكية والآمنة لبناء دخلك الرقمي وسحب أرباحك بكل سهولة وبدون تعقيد البنوك."
    )
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data == "menu_invite":
    user_id = call.from_user.id
    bot_info = bot.get_me()
    invite_link = f"https://t.me/{bot_info.username}?start={user_id}"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )

    text = (
        "🔗 *نـظـام دعـوة الأصـدقـاء الـحـصـري*\n\n"
        "شارك رابط الإحالة الخاص بك وأنشئ شبكتك الخاصة:\n"
        f"`{invite_link}`\n\n"
        "✨ كل صديق ينضم عبرك يمنحك قوة تفاعل أكبر وأرباحاً مضاعفة!"
    )
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.message_handler(
    func=lambda message: message.text
    and ("http://" in message.text or "https://" in message.text)
)
def download_video(message):
  if not check_subscription(message.from_user.id):
    bot.reply_to(message, "⚠️ عليك إتمام الاشتراكات الإجبارية أولاً لاستخدام البوت.")
    return

  url = message.text.strip()
  msg = bot.reply_to(
      message, "⏳ *جاري الاتصال بالسيرفر ومعالجة الفيديو باحترافية...*", parse_mode="Markdown"
  )

  try:
    ydl_opts = {
        "format": "best",
        "outtmpl": "downloaded_video.%(ext)s",
        "noplaylist": "True",
        "quiet": True,
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
    }

    import yt_dlp

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=True)
      filename = ydl.prepare_filename(info)

    if os.path.exists(filename):
      with open(filename, "rb") as vid:
        bot.send_video(
            message.chat.id,
            vid,
            caption="✅ *تم إنجاز التحميل بنجاح تام بواسطة Ayoub Hub*",
            parse_mode="Markdown",
        )
      os.remove(filename)
      bot.delete_message(message.chat.id, msg.message_id)
    else:
      bot.edit_message_text(
          "❌ حدث خطأ أثناء معالجة الملف.", message.chat.id, msg.message_id
      )
  except Exception as e:
    try:
      bot.edit_message_text(
          "❌ حدث خطأ، يجدر التأكد من صحة الرابط والمحاولة لاحقاً.",
          message.chat.id,
          msg.message_id,
      )
    except:
      pass


print("Ayoub Hub Legendary Edition is running perfectly via environment variables...")
bot.infinity_polling()
