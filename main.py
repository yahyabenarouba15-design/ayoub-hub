import os
import sqlite3
import telebot
from telebot import types

# التوكن مدمج مباشرة وثابت لضمان عمل كافة المزايا بدون نقصان
TOKEN = "8794061789:AAFoKPLjK287aHjSECDQ5Rc9cHFICsCwfhk".strip()
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        referred_by INTEGER
    )
"""
)
conn.commit()


def show_main_menu(chat_id, message_id=None):
  text = (
      "🌟 *مـرحـبـاً بـك فـي عـالـم Ayoub Hub الـخـارق* 🌟\n\n"
      "┏━━━━ 🎯 *الـقـائـمـة الـرئـيـسـيـة* ━━━━┓\n"
      "┃ الإمبراطورية الرقمية بين يديك الآن..\n"
      "┗━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
      "⚡ *اختر القسم الذي ترغب بالبدء فيه من الأزرار أدناه:*"
  )

  markup = types.InlineKeyboardMarkup(row_width=2)
  btn_download = types.InlineKeyboardButton(
      "📥 تحميل الفيديوهات", callback_data="download_menu"
  )
  btn_apps = types.InlineKeyboardButton(
      "🔥 التطبيقات المهكرة", callback_data="apps_menu"
  )
  btn_money = types.InlineKeyboardButton(
      "💳 البطاقات و الفيزات", callback_data="money_menu"
  )
  btn_tools = types.InlineKeyboardButton(
      "🛠 أدوات ذكية وخارقة", callback_data="tools_menu"
  )
  btn_invite = types.InlineKeyboardButton(
      "🔗 نظام الإحالة والأرباح", callback_data="invite_menu"
  )
  btn_more = types.InlineKeyboardButton(
      "📂 المزيد من الإبداعات", callback_data="more_menu"
  )

  markup.add(
      btn_download, btn_apps, btn_money, btn_tools, btn_invite, btn_more
  )

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
  args = message.text.split()
  referrer_id = None

  if len(args) > 1 and args[1].isdigit():
    ref = int(args[1])
    if ref != user_id:
      referrer_id = ref

  cursor.execute(
      "INSERT OR IGNORE INTO users (user_id, referred_by) VALUES (?, ?)",
      (user_id, referrer_id),
  )
  conn.commit()
  show_main_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
  chat_id = call.message.chat.id
  msg_id = call.message.message_id

  if call.data == "main_menu":
    show_main_menu(chat_id, msg_id)

  elif call.data == "download_menu":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = (
        "📥 *قـسـم تـحـمـيـل الـفـيـديـوهـات*\n\n"
        "أرسل أي رابط من يوتيوب، تيك توك، إنستغرام أو تويتر وسأقوم بتحميله فوراً!"
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "apps_menu":
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            "🔥 تطبيق تنزيل الفيديوهات (مهكر)",
            url="https://www.google.com",
        ),
        types.InlineKeyboardButton(
            "🚀 تليجرام بلس المعدل", url="https://www.google.com"
        ),
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        ),
    )
    text = "🔥 *قـسـم الـتـطـبـيـقـات والـعـلـوم الـمـهـكـرة*\n\nاختر التطبيق للتحميل:"
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "money_menu":
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            "💳 فيزات مجانية (رصيد 0.5$)", callback_data="sub_visas"
        ),
        types.InlineKeyboardButton(
            "🌐 فتح حساب جوجل بلاي أمريكي", callback_data="sub_gplay"
        ),
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        ),
    )
    text = (
        "💳 *قـسـم الـمـال والـبـطـاقـات*\n\nاختر الخدمة المطلوبة للمتابعة:"
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "sub_visas":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 رجوع", callback_data="money_menu")
    )
    text = (
        "💳 *قـسـم الـفـيـزات*\n\nBin: `457392xxxxxxxxxx` (فئة 0.5$ للتفعيل)."
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "sub_gplay":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 رجوع", callback_data="money_menu")
    )
    text = (
        "🌐 *حساب جوجل بلاي أمريكي*\n\nاستخدم VPN أمريكي ومسح البيانات لإنشاء الحساب."
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "tools_menu":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = (
        "🛠 *الأدوات الذكية*\n\nسيرفرات فائقة السرعة وآمنة لتجاوز القيود."
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "invite_menu":
    user_id = call.from_user.id
    bot_info = bot.get_me()
    invite_link = f"https://t.me/{bot_info.username}?start={user_id}"
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE referred_by = ?", (user_id,)
    )
    refs_count = cursor.fetchone()[0]

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = (
        "🔗 *نظام الإحالة*\n\nرابطك:\n"
        f"`{invite_link}`\n\nعدد دعواتك: *{refs_count}*"
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "more_menu":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = "📂 *المزيد*\n\nتواصل معنا عبر القنوات الرسمية."
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )


@bot.message_handler(
    func=lambda message: message.text
    and ("http://" in message.text or "https://" in message.text)
)
def download_video(message: types.Message):
  url = message.text.strip()
  msg = bot.reply_to(message, "⚡ *جاري معالجة الرابط...*", parse_mode="Markdown")

  try:
    import yt_dlp

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloaded_video.%(ext)s",
        "noplaylist": "True",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=True)
      filename = ydl.prepare_filename(info)

    if os.path.exists(filename):
      with open(filename, "rb") as vid:
        bot.send_video(message.chat.id, vid, caption="✅ تم التحميل بنجاح")
      os.remove(filename)
      bot.delete_message(message.chat.id, msg.message_id)
    else:
      bot.edit_message_text(
          "❌ حدث خطأ في معالجة الملف.", message.chat.id, msg.message_id
      )
  except Exception as e:
    bot.edit_message_text(
        "❌ تعذر التحميل، تأكد من صحة الرابط.", message.chat.id, msg.message_id
    )


print("Bot is running perfectly...")
bot.infinity_polling(skip_pending=True)
