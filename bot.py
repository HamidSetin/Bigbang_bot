import telebot
import time

TOKEN = '8604260086:AAGMYdYkNvY-sIz7dZlqjJS0Nw15AoNd__4'
bot = telebot.TeleBot(TOKEN)

# پاکسازی کامل آپدیت‌های معلق
try:
    bot.remove_webhook(drop_pending_updates=True)
except Exception:
    pass

ADMIN_IDS = [
    6202317657,      
    8304730388       
]

SUPPORT_USERNAME = "Sup_Bigbang"

FREE_ZIST_LINK = "https://t.me/Bigbangzist"  
FREE_SHIMI_LINK = "https://t.me/Bigbangchem"  

prices = {
    "buy_zist": ("بانک تست زیست جامع", "400,000"),
    "shimi": ("بانک تست شیمی جامع", "360,000"),
    "fizik": ("بانک تست فیزیک جامع", "330,000"),
    "math": ("بانک تست ریاضی جامع", "360,000"),
    "full_4": ("پکیج کامل هر ۴ بانک تست", "1,250,000")
}

user_selected_product = {}

def get_main_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("🧬 بانک تست زیست جامع - 400,000 تومان", callback_data="buy_zist"))
    markup.row(telebot.types.InlineKeyboardButton("🧪 بانک تست شیمی جامع - 360,000 تومان", callback_data="shimi"))
    markup.row(telebot.types.InlineKeyboardButton("💡 بانک تست فیزیک جامع - 330,000 تومان", callback_data="fizik"))
    markup.row(telebot.types.InlineKeyboardButton("📐 بانک تست ریاضی جامع - 360,000 تومان", callback_data="math"))
    markup.row(telebot.types.InlineKeyboardButton("📦 پکیج کامل هر ۴ بانک تست - 1,250,000 تومان", callback_data="full_4"))
    return markup

def get_persistent_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("🚀 منوی اصلی / شروع"))
    keyboard.add(
        telebot.types.KeyboardButton("🎁 زیست پارسال (رایگان)"),
        telebot.types.KeyboardButton("🎁 شیمی پارسال (رایگان)")
    )
    keyboard.add(
        telebot.types.KeyboardButton("💬 ارتباط با پشتیبانی"),
        telebot.types.KeyboardButton("توضیحات بانک تست‌ها 📚")
    )
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "سلام! به ربات بیگ بنگ خوش آمدید.\n\n🔥 **جشنواره تخفیف ویژه تا جمعه ۳ مهر**\nمحصول مورد نظرت رو از منوی زیر انتخاب کن:", 
        reply_markup=get_main_markup(), 
        parse_mode="Markdown"
    )
    bot.send_message(
        message.chat.id,
        "👇 دسترسی سریع به منوها و آرشیوهای رایگان از طریق دکمه‌های پایین صفحه:",
        reply_markup=get_persistent_keyboard()
    )

# هندلر اختصاصی برای دکمه‌های خرید با دیکشنری مشخص
@bot.callback_query_handler(func=lambda call: call.data in prices)
def handle_buy_callback(call):
    print(f"DEBUG: Buy button clicked -> {call.data}")
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass
    
    item_name, price = prices[call.data]
    user_selected_product[call.from_user.id] = item_name
    
    text = (
        f"💳 خرید {item_name}\n\n"
        f"💰 مبلغ قابل پرداخت: {price} تومان (تخفیف ویژه تا ۳ مهر)\n\n"
        f"شماره کارت: `5022291535771289` به نام سیدحمیدرضامحسنی راد\n\n"
        "لطفاً واریز کن و عکس فیش رو همینجا بفرست تا بررسی کنم."
    )
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            text=text, 
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Edit text error: {e}")

# هندلر اختصاصی برای تأیید فیش توسط ادمین
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def handle_approve_callback(call):
    print(f"DEBUG: Approve button clicked -> {call.data}")
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass
        
    if call.from_user.id not in ADMIN_IDS:
        try:
            bot.answer_callback_query(call.id, "❌ شما دسترسی ادمین ندارید!", show_alert=True)
        except:
            pass
        return
        
    user_id = int(call.data.split("_")[1])
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    try:
        bot.send_message(
            user_id, 
            "✅ فیش واریزی شما تایید شد!\nبرای دریافت لینک دسترسی با پشتیبانی در ارتباط باشید:", 
            reply_markup=user_markup
        )
    except Exception as e:
        print(f"User send error: {e}")
    
    try:
        bot.edit_message_caption(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            caption=call.message.caption + "\n\n🟢 وضعیت: تایید شد توسط ادمین", 
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Caption edit error: {e}")

@bot.message_handler(content_types=['photo', 'document'])
def handle_receipt(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    
    chat_info = f"@{username}" if username else "بدون آیدی"
    product_purchased = user_selected_product.get(user_id, "نامشخص / از منو انتخاب نشده")
    
    markup = telebot.types.InlineKeyboardMarkup()
    if username:
        markup.add(telebot.types.InlineKeyboardButton("💬 چت مستقیم با کاربر", url=f"https://t.me/{username}"))
    markup.add(telebot.types.InlineKeyboardButton("✅ تایید فیش (بررسی شد)", callback_data=f"approve_{user_id}"))
    
    caption = (
        f"📩 فیش واریزی جدید!\n\n"
        f"📦 محصول درخواستی: {product_purchased}\n"
        f"👤 نام: {user_name}\n"
        f"🔗 آیدی: {chat_info}\n"
        f"🆔 آی‌دی عددی: `{user_id}`\n\n"
        "برای تایید روی دکمه زیر بزنید."
    )
    
    if message.photo:
        file_id = message.photo[-1].file_id
        for admin_id in ADMIN_IDS:
            try:
                bot.send_photo(admin_id, file_id, caption=caption, reply_markup=markup, parse_mode="Markdown")
            except Exception as e:
                print(f"Admin photo error: {e}")
    elif message.document:
        file_id = message.document.file_id
        for admin_id in ADMIN_IDS:
            try:
                bot.send_document(admin_id, file_id, caption=caption, reply_markup=markup, parse_mode="Markdown")
            except Exception as e:
                print(f"Admin doc error: {e}")
    
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    bot.send_message(
        message.chat.id, 
        f"✅ فیش شما برای خرید **{product_purchased}** دریافت شد.\nپس از بررسی توسط مدیریت، دسترسی ارسال خواهد شد.",
        reply_markup=user_markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text in [
    "🚀 منوی اصلی / شروع", 
    "💬 ارتباط با پشتیبانی", 
    "توضیحات بانک تست‌ها 📚", 
    "🎁 زیست پارسال (رایگان)", 
    "🎁 شیمی پارسال (رایگان)"
])
def handle_persistent_buttons(message):
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 چت با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    if message.text == "🚀 منوی اصلی / شروع":
        bot.send_message(
            message.chat.id,
            "سلام دوباره! به منوی اصلی برگشتیم. محصول مورد نظرت رو انتخاب کن:",
            reply_markup=get_main_markup()
        )
    elif message.text == "🎁 زیست پارسال (رایگان)":
        free_zist_markup = telebot.types.InlineKeyboardMarkup()
        free_zist_markup.add(telebot.types.InlineKeyboardButton("🔗 ورود به کانال زیست پارسال", url=FREE_ZIST_LINK))
        bot.send_message(
            message.chat.id,
            "🎁 این هم هدیه شما؛ برای دریافت بانک تست زیست پارسال به صورت کاملاً رایگان، روی دکمه زیر بزنید:",
            reply_markup=free_zist_markup
        )
    elif message.text == "🎁 شیمی پارسال (رایگان)":
        free_shimi_markup = telebot.types.InlineKeyboardMarkup()
        free_shimi_markup.add(telebot.types.InlineKeyboardButton("🔗 ورود به کانال شیمی پارسال", url=FREE_SHIMI_LINK))
        bot.send_message(
            message.chat.id,
            "🎁 این هم هدیه شما؛ برای دریافت بانک تست شیمی پارسال به صورت کاملاً رایگان، روی دکمه زیر بزنید:",
            reply_markup=free_shimi_markup
        )
    elif message.text == "💬 ارتباط با پشتیبانی":
        bot.send_message(
            message.chat.id,
            "برای ارتباط مستقیم با پشتیبانی و پرسیدن سوالات خود، روی دکمه زیر بزنید:",
            reply_markup=user_markup
        )
    elif message.text == "توضیحات بانک تست‌ها 📚":
        bot.send_message(
            message.chat.id,
            "🔥 پرواز به سمت درصد ۱۰۰ با بانک تست‌های خفنِ «بیگ‌بنگ»! 🔥\n\n"
            "رفیق، اگر دنبال اینی که تو کنکور بترکونی و دیگه توی درس‌های اختصاصی لنگ هیچ منبعی نباشی، درست اومدی! ما اینجا گلِ سرسبدِ سوالات آزمون‌های معتبر کشور رو برات یکجا جمع کردیم تا هیچ نکته‌ای از دستت در نره. 🎯\n\n"
            "📌 تو این پکیج چی داریم؟\n\n"
            "🧬 زیست‌شناسی:\n"
            "🔹 ماز (سالیانه و پرمیوم) | زیستاز (سالیانه و پیشرفته) | خیلی سبز (سالیانه و پلاس) | آرمان\n\n"
            "🧪 شیمی:\n"
            "🔹 قلم‌چی | ماز | ماراتون | خیلی سبز\n\n"
            "⚗️ فیزیک:\n"
            "🔹 قلم‌چی | ماز | ماراتون | خیلی سبز | مدارس برتر\n\n"
            "📐 ریاضی:\n"
            "🔹 قلم‌چی | ماراتون | خیلی سبز | ماز | مدارس برتر | آلفا\n\n"
            "🚀 چرا بانک تست بیگ‌بنگ بی‌رقیبه؟\n\n"
            "💯 پوشش صددرصدی: تمام مباحث، فعالیت‌ها و ریزبه‌ریزِ تمرین‌های کتاب درسی رو شخم زدیم؛ هیچ چیزی از قلم نیفتفته!\n\n"
            "🧠 توسط رتبه‌برترها و طراحان: سوالات توسط رتبه‌های برتر کنکور و طراحان مطرح آزمون‌ها گلچین شدن تا کیفیت کار صددرصد تضمینی باشه.\n\n"
            "👇 همین الان از منوی بالا محصول مورد نظرت رو انتخاب کن:",
            reply_markup=user_markup
        )

@bot.message_handler(func=lambda message: True)
def handle_text_fallback(message):
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    bot.send_message(
        message.chat.id,
        "⚠️ لطفاً برای ارسال فیش واریزی، **فقط عکس یا اسکرین‌شات فیش** را ارسال کنید.",
        reply_markup=user_markup
    )

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=30)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(3)
