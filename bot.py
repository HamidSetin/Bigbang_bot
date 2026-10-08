import telebot
import time
import requests

TOKEN = '8604260086:AAGMYdYkNvY-sIz7dZlqjJS0Nw15AoNd__4'

# پاک کردن مستقیم وب‌هوک و آپدیت‌های معلق برای آزادسازی ربات از دست نمونه‌های قبلی
try:
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
except Exception as e:
    print(f"Direct webhook delete error: {e}")

bot = telebot.TeleBot(TOKEN)

ADMIN_IDS = [
    6202317657,      
    8304730388       
]

SUPPORT_USERNAME = "Sup_Bigbang"
FREE_ZIST_LINK = "https://t.me/Bigbangzist"  
FREE_SHIMI_LINK = "https://t.me/Bigbangchem"  

PERSISTENT_BUTTONS = [
    "منوی اصلی / شروع", 
    "ارتباط با پشتیبانی", 
    "توضیحات بانک تست‌ها", 
    "زیست پارسال (رایگان)", 
    "شیمی پارسال (رایگان)"
]

cash_prices = {
    "cash_zist": ("بانک تست زیست جامع (نقدی)", "400,000"),
    "cash_shimi": ("بانک تست شیمی جامع (نقدی)", "360,000"),
    "cash_fizik": ("بانک تست فیزیک جامع (نقدی)", "330,000"),
    "cash_math": ("بانک تست ریاضی جامع (نقدی)", "360,000"),
    "cash_full": ("پکیج کامل هر ۴ بانک تست (نقدی)", "1,250,000")
}

installment_prices = {
    "inst_full": ("پکیج کامل هر ۴ بانک تست (اقساطی)", "600,000 تومان (قسط اول از کل ۱,۶۰۰,۰۰۰ تومان - دو قسط بعدی هر کدام ۵۰۰,۰۰۰ تومان)")
}

user_selected_product = {}
user_phones = {}

DESCRIPTION_TEXT = (
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
    "💯 پوشش صددرصدی: تمام مباحث، فعالیت‌ها و ریزبه‌ریزِ تمرین‌های کتاب درسی رو شخم زدیم؛ هیچ چیزی از قلم نیفتفته!\n\n"
    "🧠 توسط رتبه‌برترها و طراحان: سوالات توسط رتبه‌های برتر کنکور و طراحان مطرح آزمون‌ها گلچین شدن تا کیفیت کار صددرصد تضمینی باشه.\n\n"
    "📈 همگام با سختی کنکور: سوالات دقیقاً متناسب با سطح دشواری کنکور طراحی شدن تا توی جلسه آزمون هیچ سورپرایزی برات وجود نداشته باشه.\n\n"
    "💪 برای چه سطحی مناسبه؟\n"
    "• پایه متوسط و قوی داری؟ ازت یه غولِ بی‌رقیب می‌سازیم!\n"
    "• پایه ضعیفی داری؟ کاری می‌کنیم خودت با دیدن پیشرفتت شاخ درآری!\n\n"
    "🛡 خیالت راحتِ راحت؛ تضمین ۱۰۰ درصدی!\n"
    "انقدر از کارمون مطمئنیم که تضمین برگشت وجه در صورت نارضایتی گذاشتیم تا با خیالِ تختِ تخت خرید کنی.\n\n"
    "💡 با این بانک تست، پرونده‌ی کتاب‌های کمک‌درسی قطور و گیج‌کننده برای همیشه بسته میشه و کاملاً بی‌نیاز میشی.\n\n"
    "👇 همین الان نوع خرید خود رو انتخاب کن:"
)

def get_main_menu_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("خرید نقدی (آنی با تخفیف ویژه)", callback_data="mode_cash"))
    markup.row(telebot.types.InlineKeyboardButton("خرید اقساطی (ویژه پکیج کامل)", callback_data="mode_installment"))
    return markup

def get_cash_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("زیست جامع - 400,000 تومان", callback_data="cash_zist"))
    markup.row(telebot.types.InlineKeyboardButton("شیمی جامع - 360,000 تومان", callback_data="cash_shimi"))
    markup.row(telebot.types.InlineKeyboardButton("فیزیک جامع - 330,000 تومان", callback_data="cash_fizik"))
    markup.row(telebot.types.InlineKeyboardButton("ریاضی جامع - 360,000 تومان", callback_data="cash_math"))
    markup.row(telebot.types.InlineKeyboardButton("پکیج کامل ۴ درس - 1,250,000 تومان", callback_data="cash_full"))
    markup.row(telebot.types.InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="back_to_main"))
    return markup

def get_installment_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("پکیج کامل اقساطی (قسط اول ۶۰۰ تومانی)", callback_data="inst_full"))
    markup.row(telebot.types.InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="back_to_main"))
    return markup

def get_persistent_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("منوی اصلی / شروع"))
    keyboard.add(
        telebot.types.KeyboardButton("زیست پارسال (رایگان)"),
        telebot.types.KeyboardButton("شیمی پارسال (رایگان)")
    )
    keyboard.add(
        telebot.types.KeyboardButton("ارتباط با پشتیبانی"),
        telebot.types.KeyboardButton("توضیحات بانک تست‌ها")
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

@bot.message_handler(func=lambda message: message.text in PERSISTENT_BUTTONS)
def handle_persistent_buttons(message):
    try:
        if message.text == "منوی اصلی / شروع":
            bot.send_message(
                message.chat.id,
                "سلام دوباره! به منوی اصلی برگشتیم. لطفاً نوع خرید خود را انتخاب کنید:",
                reply_markup=get_main_menu_markup()
            )
        elif message.text == "زیست پارسال (رایگان)":
            free_zist_markup = telebot.types.InlineKeyboardMarkup()
            free_zist_markup.add(telebot.types.InlineKeyboardButton("ورود به کانال زیست پارسال", url=FREE_ZIST_LINK))
            bot.send_message(
                message.chat.id,
                "این هم هدیه شما؛ برای دریافت بانک تست زیست پارسال به صورت کاملاً رایگان، روی دکمه زیر بزنید:",
                reply_markup=free_zist_markup
            )
        elif message.text == "شیمی پارسال (رایگان)":
            free_shimi_markup = telebot.types.InlineKeyboardMarkup()
            free_shimi_markup.add(telebot.types.InlineKeyboardButton("ورود به کانال شیمی پارسال", url=FREE_SHIMI_LINK))
            bot.send_message(
                message.chat.id,
                "این هم هدیه شما؛ برای دریافت بانک تست شیمی پارسال به صورت کاملاً رایگان، روی دکمه زیر بزنید:",
                reply_markup=free_shimi_markup
            )
        elif message.text == "ارتباط با پشتیبانی":
            user_markup = telebot.types.InlineKeyboardMarkup()
            user_markup.add(telebot.types.InlineKeyboardButton("چت با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
            bot.send_message(
                message.chat.id,
                "برای ارتباط مستقیم با پشتیبانی و پرسیدن سوالات خود، روی دکمه زیر بزنید:",
                reply_markup=user_markup
            )
        elif message.text == "توضیحات بانک تست‌ها":
            bot.send_message(
                message.chat.id,
                DESCRIPTION_TEXT,
                reply_markup=get_main_menu_markup()
            )
    except Exception as e:
        print(f"Persistent button error: {e}")

@bot.callback_query_handler(func=lambda call: call.data in ["mode_cash", "mode_installment", "back_to_main"])
def handle_mode_selection(call):
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass
    
    if call.data == "mode_cash":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="بخش خرید نقدی (آنی با تخفیف‌های ویژه تا جمعه ۱۷ مهر)\n\
