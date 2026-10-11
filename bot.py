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
                "رفیق، اگر دنبال اینی که تو کنکور بترکونی و دیگه توی درس‌های اختصاصی لنگ هیچ منبعی نباشی، درست اومدی! ما اینجا گلِ سرسبدِ سوالات آزمون‌های معتبر کشور رو برات یکجا جمع کردیم تا هیچ نکته‌ای از دستت در نره. 🎯\n\n"
                "📌 تو این پکیج چی داریم؟\n\n"
                "🧬 زیست‌شناسی:\n"
                "- ماز (سالیانه و پرمیوم)\n"
                "- زیستاز (سالیانه و پیشرفته)\n"
                "- خیلی سبز (سالیانه و پلاس)\n"
                "- آرمان\n\n"
                "🧪 شیمی:\n"
                "- قلم‌چی\n"
                "- ماز\n"
                "- ماراتون\n"
                "- خیلی سبز\n\n"
                "⚗️ فیزیک:\n"
                "- قلم‌چی\n"
                "- ماز\n"
                "- ماراتون\n"
                "- خیلی سبز\n"
                "- مدارس برتر\n\n"
                "📐 ریاضی:\n"
                "- قلم‌چی\n"
                "- ماراتون\n"
                "- خیلی سبز\n"
                "- ماز\n"
                "- مدارس برتر\n"
                "- آلفا\n\n"
                "🚀 چرا بانک تست بیگ‌بنگ بی‌رقیبه؟\n\n"
                "💯 پوشش صددرصدی: تمام مباحث، فعالیت‌ها و ریزبه‌ریزِ تمرین‌های کتاب
