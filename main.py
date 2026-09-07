import os
import sqlite3
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# إعداد قاعدة البيانات الشاملة
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


# القائمة الرئيسية الفخمة
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

  # 1. قسم التحميل الخارق
  elif call.data == "download_menu":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = (
        "📥 *قـسـم تـحـمـيـل الـفـيـديـوهـات الـشـامـل*\n\n"
        "أرسل أي رابط من:\n"
        "• يوتيوب (YouTube)\n"
        "• تيك توك (TikTok بدون علامة مائية)\n"
        "• إنستغرام (Instagram)\n"
        "• تويتر / إكس (Twitter)\n\n"
        "⚡ *وسيقوم السيرفر بمعالجته وتحميله فوراً وبأقصى سرعة!*"
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  # 2. قسم التطبيقات المهكرة (روابط إعلانية لكسب المال)
  elif call.data == "apps_menu":
    markup = types.InlineKeyboardMarkup(row_width=1)
    # استبدل الروابط أدناه بروابط مختصرة أو روابط إعلانية خاصة بك (مثل Adsterra أو Monetag) لتستفيد مالياً
    markup.add(
        types.InlineKeyboardButton(
            "🔥 تطبيق تنزيل الفيديوهات الخارق (مهكر)",
            url="https://your-ad-link.com/app1",
        ),
        types.InlineKeyboardButton(
            "🚀 تطبيق تليجرام بلس المعدل (بدون إعلانات)",
            url="https://your-ad-link.com/app2",
        ),
        types.InlineKeyboardButton(
            "💎 ألعاب مهكرة بروابط مباشرة وسريعة",
            url="https://your-ad-link.com/games",
        ),
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        ),
    )
    text = (
        "🔥 *قـسـم الـتـطـبـيـقـات والـعـلـوم الـمـهـكـرة*\n\n"
        "اختر التطبيق الذي تريده، واضغط على الرابط للتحميل المباشر الآمن والسرعة الفائقة 🚀"
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  # 3. قسم الفيزات وبطاقات جوجل وفتح الحسابات
  elif call.data == "money_menu":
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            "💳 شحن فيزات مجانية (رصيد 0.5 دولار)",
            callback_data="sub_visas",
        ),
        types.InlineKeyboardButton(
            "🌐 طريقة فتح حساب جوجل بلاي أمريكي دائم",
            callback_data="sub_gplay",
        ),
        types.InlineKeyboardButton(
            "🎁 بطاقات جوجل بلاي وهدايا أسبوعية",
            url="https://your-ad-link.com/giftcards",
        ),
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        ),
    )
    text = (
        "💳 *قـسـم الـمـال والـبـطـاقـات والـفـيـزات*\n\n"
        "اختر الخدمة المطلوبة للبدء في تحقيق الأرباح وبناء حسابات رقمية احترافية."
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "sub_visas":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 رجوع للقسام", callback_data="money_menu")
    )
    text = (
        "💳 *قـسـم الـفـيـزات والـبـطـاقـات الـمـجـانـية*\n\n"
        "• تم تخصيص فيزات بفئات (0.5$ للتفعيل السريع).\n"
        "• *Bin:* `457392xxxxxxxxxx`\n"
        "• استخدم مواقع الفحص (Checkers) لتفعيلها على الحسابات الوهمية."
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  elif call.data == "sub_gplay":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 رجوع للقسم", callback_data="money_menu")
    )
    text = (
        "🌐 *إرشادات فتح حساب جوجل بلاي أمريكي*\n\n"
        "1. استخدم تطبيق VPN قوي على دولة أمريكا.\n"
        "2. امسح بيانات متجر جوجل بلاي.\n"
        "3. انشئ حساب جيميل جديد من داخل المتجر وستظهر لك العملة بالدولار ($) فوراً."
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  # 4. قسم الأدوات الخارقة وتجاوز الحدود
  elif call.data == "tools_menu":
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        )
    )
    text = (
        "🛠 *قـسـم الأدوات الـذكـيـة وتـجـاوز الـحـدود*\n\n"
        "• *السرعة:* سيرفرات سحابية فائقة الأداء لا تعاني من الثقل أو التوقف.\n"
        "• *الأمان:* تشفير تام واتصال آمن لتجاوز الحظر والقيود الجغرافية.\n"
        "• *استرجاع الصور والملفات:* قريباً سيتم إطلاق ميزة فحص واستعادة الملفات المحذوفة بنقرة واحدة!"
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  # 5. نظام دعوة الأصدقاء والأرباح
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
        "🔗 *نـظـام الإحـالـة والـربـح الـمـضـاعـف*\n\n"
        "شارك رابطك الخاص مع أصدقائك وفي المجموعات:\n"
        f"`{invite_link}`\n\n"
        f"👥 عدد الأشخاص الذين دعيتهم: *{refs_count} صديق*\n"
        "💎 كلما زاد عدد المدعوين، كلما حصلت على صلاحيات حصرية وأرباح أعلى!"
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )

  # 6. قسم المزيد (قائمة فرعية عميقة)
  elif call.data == "more_menu":
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            "💬 قروب الدعم والمجتمع الخارق",
            url="https://t.me/your_support_group",
        ),
        types.InlineKeyboardButton(
            "📢 قناة الإشعارات والتحديثات", url="https://t.me/your_channel"
        ),
        types.InlineKeyboardButton(
            "⭐ تقييم البوت ودعم المطور", url="https://t.me/your_bot"
        ),
        types.InlineKeyboardButton(
            "🔙 القائمة الرئيسية", callback_data="main_menu"
        ),
    )
    text = (
        "📂 *قـسـم الـمـزيـد والـخـدمـات الإضـافـيـة*\n\n"
        "هنا تجد كل روابط التواصل الاجتماعي، قنوات الدعم الفني، والتحديثات المستمرة لإمبراطورية Ayoub Hub."
    )
    bot.edit_message_text(
        text, chat_id, msg_id, reply_markup=markup, parse_mode="Markdown"
    )


# نظام معالجة وتحميل الفيديوهات الخارق (بدون ثقل أو توقف)
@bot.message_handler(
    func=lambda message: message.text
    and ("http://" in message.text or "https://" in message.text)
)
def download_video(message):
  url = message.text.strip()
  msg = bot.reply_to(
      message,
      "⚡ *جاري اختراق السيرفر ومعالجة الرابط بسرعة فائقة...*",
      parse_mode="Markdown",
  )

  try:
    ydl_opts = {
        "format": "best/bestvideo+bestaudio",
        "outtmpl": "downloaded_video.%(ext)s",
        "noplaylist": "True",
        "quiet": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "web"],
            }
        },
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
            caption=(
                "✅ *تم التحميل بنجاح تام بواسطة إمبراطورية Ayoub Hub*\n🔗 رابط"
                f" إحالتك لدعوة أصدقائك: `https://t.me/{bot.get_me().username}?start={message.from_user.id}`"
            ),
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
          "❌ حدث خطأ في السيرفر أو أن الرابط محمي، يجدر المحاولة برابط آخر.",
          message.chat.id,
          msg.message_id,
      )
    except:
      pass


print("Ayoub Hub Ultimate Imperial Edition is running at maximum speed...")
bot.infinity_polling()
