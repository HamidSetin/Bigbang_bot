import telebot
import time

TOKEN = '8604260086:AAGMYdYkNvY-sIz7dZlqjJS0Nw15AoNd__4'
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

def get_main_menu_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("💰 خرید نقدی (آنی با تخفیف ویژه)", callback_data="mode_cash"))
    markup.row(telebot.types.InlineKeyboardButton("📅 خرید اقساطی (ویژه پکیج کامل)", callback_data="mode_installment"))
    return markup

def get_cash_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("🧬 زیست جامع - 400,000 تومان", callback_data="cash_zist"))
    markup.row(telebot.types.InlineKeyboardButton("🧪 شیمی جامع - 360,000 تومان", callback_data="cash_shimi"))
    markup.row(telebot.types.InlineKeyboardButton("💡 فیزیک جامع - 330,000 تومان", callback_data="cash_fizik"))
    markup.row(telebot.types.InlineKeyboardButton("📐 ریاضی جامع - 360,000 تومان", callback_data="cash_math"))
    markup.row(telebot.types.InlineKeyboardButton("📦 پکیج کامل ۴ درس - 1,250,000 تومان", callback_data="cash_full"))
    markup.row(telebot.types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_main"))
    return markup

def get_installment_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("📦 پکیج کامل اقساطی (قسط اول ۶۰۰ تومانی)", callback_data="inst_full"))
    markup.row(telebot.types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_main"))
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
    try:
        bot.send_message(
            message.chat.id, 
            "سلام! به ربات بانک تست «بیگ‌بنگ» خوش آمدید. 🚀\n\nلطفاً نوع خرید خود را انتخاب کنید:", 
            reply_markup=get_main_menu_markup(), 
            parse_mode="Markdown"
        )
        bot.send_message(
            message.chat.id,
            "👇 دسترسی سریع به منوها و آرشیوهای رایگان از طریق دکمه‌های پایین صفحه:",
            reply_markup=get_persistent_keyboard()
        )
    except Exception as e:
        print(f"Start command error: {e}")

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
                text="💰 **بخش خرید نقدی (آنی با تخفیف‌های ویژه تا جمعه ۱۷ مهر)**\n\nمحصول مورد نظر خود را انتخاب کنید:",
                reply_markup=get_cash_markup(),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Edit cash menu error: {e}")
            
    elif call.data == "mode_installment":
        if call.from_user.id not in user_phones:
            contact_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            contact_markup.add(telebot.types.KeyboardButton("📞 اشتراک‌‌گذاری شماره تلفن برای خرید اقساطی", request_contact=True))
            
            try:
                bot.send_message(
                    call.message.chat.id,
                    "📌 برای
