import telebot
import time

TOKEN = '8604260086:AAEu2JmITKN-nYHriiCY5N_pw550hHLia5o'
bot = telebot.TeleBot(TOKEN)

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

cash_prices = {
    "cash_zist": ("بانک تست زیست جامع (نقدی)", "499,000"),
    "cash_shimi": ("بانک تست شیمی جامع (نقدی)", "449,000"),
    "cash_fizik": ("بانک تست فیزیک جامع (نقدی)", "419,000"),
    "cash_math": ("بانک تست ریاضی جامع (نقدی)", "449,000"),
    "cash_full": ("پکیج کامل هر ۴ بانک تست (نقدی)", "1,500,000")
}

installment_prices = {
    "inst_full": ("پکیج کامل هر ۴ بانک تست (اقساطی)", "۶۰۰,۰۰۰ تومان (قسط اول از کل ۱,۸۰۰,۰۰۰ تومان - دو قسط بعدی هر کدام ۶۰۰,۰۰۰ تومان)")
}

user_selected_product = {}
user_phones = {}

def get_main_menu_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("💳 خرید نقدی", callback_data="mode_cash"))
    markup.row(telebot.types.InlineKeyboardButton("🤝 خرید اقساطی (ویژه پکیج کامل)", callback_data="mode_installment"))
    return markup

def get_cash_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("🧬 زیست جامع - 499,000 تومان", callback_data="cash_zist"))
    markup.row(telebot.types.InlineKeyboardButton("🧪 شیمی جامع - 449,000 تومان", callback_data="cash_shimi"))
    markup.row(telebot.types.InlineKeyboardButton("⚗️ فیزیک جامع - 419,000 تومان", callback_data="cash_fizik"))
    markup.row(telebot.types.InlineKeyboardButton("📐 ریاضی جامع - 449,000 تومان", callback_data="cash_math"))
    markup.row(telebot.types.InlineKeyboardButton("🔥 پکیج کامل ۴ درس - 1,500,000 تومان", callback_data="cash_full"))
    markup.row(telebot.types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_main"))
    return markup

def get_installment_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("💎 پکیج کامل اقساطی (قسط اول ۶۰۰ تومانی)", callback_data="inst_full"))
    markup.row(telebot.types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_main"))
    return markup

def get_persistent_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("🏠 منوی اصلی / شروع"))
    keyboard.add(
        telebot.types.KeyboardButton("🎁 زیست پارسال (رایگان)"),
        telebot.types.KeyboardButton("🎁 شیمی پارسال (رایگان)")
    )
    keyboard.add(
        telebot.types.KeyboardButton("📞 ارتباط با پشتیبانی"),
        telebot.types.KeyboardButton("📖 توضیحات بانک تست‌ها")
    )
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.send_message(
            message.chat.id, 
            "سلام! به ربات بانک تست بیگ‌بنگ خوش آمدید. لطفاً نوع خرید خود را انتخاب کنید:", 
            reply_markup=get_main_menu_markup()
        )
        bot.send_message(
            message.chat.id,
            "دسترسی سریع به منوها و آرشیوهای رایگان از طریق دکمه‌های پایین صفحه:",
            reply_markup=get_persistent_keyboard()
        )
    except Exception as e:
        print(f"Start command error: {e}")

@bot.message_handler(content_types=['text'], func=lambda message: message.text in [
    "🏠 منوی اصلی / شروع", 
    "📞 ارتباط با پشتیبانی", 
    "📖 توضیحات بانک تست‌ها", 
    "🎁 زیست پارسال (رایگان)", 
    "🎁 شیمی پارسال (رایگان)"
])
def handle_persistent_buttons(message):
    try:
        if message.text == "🏠 منوی اصلی / شروع":
            bot.send_message(
                message.chat.id,
                "سلام دوباره! به منوی اصلی برگشتیم. لطفاً نوع خرید خود را انتخاب کنید:",
                reply_markup=get_main_menu_markup()
            )
        elif message.text == "🎁 زیست پارسال (رایگان)":
            free_zist_markup = telebot.types.InlineKeyboardMarkup()
            free_zist_markup.add(telebot.types.InlineKeyboardButton("🚀 ورود به کانال زیست پارسال", url=FREE_ZIST_LINK))
            bot.send_message(
                message.chat.id,
                "این هم هدیه شما؛ برای دریافت بانک تست زیست پارسال به صورت کاملاً رایگان، روی دکمه زیر بزنید:",
                reply_markup=free_zist_markup
            )
        elif message.text == "🎁 شیمی پارسال (رایگان)":
            free_shimi_markup = telebot.types.InlineKeyboardMarkup()
            free_shimi_markup.add(telebot.types.InlineKeyboardButton("🚀 ورود به کانال شیمی پارسال", url=FREE_SHIMI_LINK))
            bot.send_message(
                message.chat.id,
                "این هم هدیه شما؛ برای دریافت بانک تست شیمی پارسال به صورت کاملاً رایگان، روی دکمه زیر بزنید:",
                reply_markup=free_shimi_markup
            )
        elif message.text == "📞 ارتباط با پشتیبانی":
            user_markup = telebot.types.InlineKeyboardMarkup()
            user_markup.add(telebot.types.InlineKeyboardButton("💬 چت با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
            bot.send_message(
                message.chat.id,
                "برای ارتباط مستقیم با پشتیبانی و پرسیدن سوالات خود، روی دکمه زیر بزنید:",
                reply_markup=user_markup
            )
        elif message.text == "📖 توضیحات بانک تست‌ها":
            description_text = (
                "🔥 پرواز به سمت درصد ۱۰۰ با بانک تست‌های خفنِ «بیگ‌‌بنگ»! 🔥\n\n"
                "گلچینی از بهترین سوالات آزمون‌های معتبر (ماز، زیستاز، قلم‌چی، خیلی سبز و مدارس برتر) پوشش صددرصدی مباحث کنکور.\n\n"
                "👇 همین الان نوع خرید خود رو انتخاب کن:"
            )
            bot.send_message(
                message.chat.id,
                description_text,
                reply_markup=get_main_menu_markup()
            )
    except Exception as e:
        print(f"Persistent button error: {e}")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact:
        user_phones[message.from_user.id] = message.contact.phone_number
        try:
            bot.send_message(
                message.chat.id,
                f"✅ شماره تلفن شما ({message.contact.phone_number}) با موفقیت ثبت شد.",
                reply_markup=get_persistent_keyboard()
            )
            bot.send_message(
                message.chat.id,
                (
                    "🤝 بخش خرید اقساطی ویژه پکیج کامل\n\n"
                    "💰 قیمت کل: ۱,۸۰۰,۰۰۰ تومان\n"
                    "📋 شرایط پرداخت: قسط اول ۶۰۰,۰۰۰ تومان (همین الان) + دو قسط بعدی هر کدام ۶۰۰,۰۰۰ تومان\n\n"
                    "محصول خود را انتخاب کنید:"
                ),
                reply_markup=get_installment_markup()
            )
        except Exception as e:
            print(f"Contact handler error: {e}")

@bot.message_handler(content_types=['photo', 'document'])
def handle_receipt(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    
    chat_info = f"@{username}" if username else "بدون آیدی"
    product_purchased = user_selected_product.get(user_id, "نامشخص")
    phone = user_phones.get(user_id, "ثبت نشده")
    
    markup = telebot.types.InlineKeyboardMarkup()
    if username:
        markup.add(telebot.types.InlineKeyboardButton("💬 چت مستقیم با کاربر", url=f"https://t.me/{username}"))
    markup.add(telebot.types.InlineKeyboardButton("✅ تایید فیش", callback_data=f"approve_{user_id}"))
    
    caption = (
        f"🚨 فیش واریزی جدید!\n\n"
        f"📦 محصول: {product_purchased}\n"
        f"👤 نام: {user_name}\n"
        f"🔗 آیدی: {chat_info}\n"
        f"📱 شماره تماس: {phone}\n"
        f"🆔 آیدی عددی: {user_id}\n\n"
        "برای تایید روی دکمه زیر بزنید."
    )
    
    if message.photo:
        file_id = message.photo[-1].file_id
        for admin_id in ADMIN_IDS:
            try:
                bot.send_photo(admin_id, file_id, caption=caption, reply_markup=markup)
            except Exception as e:
                print(f"Admin photo error: {e}")
    elif message.document:
        file_id = message.document.file_id
        for admin_id in ADMIN_IDS:
            try:
                bot.send_document(admin_id, file_id, caption=caption, reply_markup=markup)
            except Exception as e:
                print(f"Admin doc error: {e}")
    
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    try:
        bot.send_message(
            message.chat.id, 
            f"✅ فیش شما برای {product_purchased} دریافت شد. پس از بررسی توسط مدیریت، دسترسی ارسال خواهد شد.",
            reply_markup=user_markup
        )
    except Exception as e:
        print(f"User receipt ack error: {e}")

@bot.callback_query_handler(func=lambda call: call.data in ["mode_cash", "mode_installment", "back_to_main"])
def handle_mode_selection(call):
    try:
        bot.answer_callback_query(call.
