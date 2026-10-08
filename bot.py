import telebot
import time

TOKEN = '8604260086:AAGMYdYkNvY-sIz7dZlqjJS0Nw15AoNd__4'
bot = telebot.TeleBot(TOKEN)

# پاک کردن کامل وب‌هوک و آپدیت‌های معلق برای جلوگیری از خطای 409 Conflict
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
    markup.row(telebot.types.InlineKeyboardButton("💳 خرید نقدی (آنی با تخفیف ویژه)", callback_data="mode_cash"))
    markup.row(telebot.types.InlineKeyboardButton("🤝 خرید اقساطی (ویژه پکیج کامل)", callback_data="mode_installment"))
    return markup

def get_cash_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("🧬 زیست جامع - 400,000 تومان", callback_data="cash_zist"))
    markup.row(telebot.types.InlineKeyboardButton("🧪 شیمی جامع - 360,000 تومان", callback_data="cash_shimi"))
    markup.row(telebot.types.InlineKeyboardButton("⚗️ فیزیک جامع - 330,000 تومان", callback_data="cash_fizik"))
    markup.row(telebot.types.InlineKeyboardButton("📐 ریاضی جامع - 360,000 تومان", callback_data="cash_math"))
    markup.row(telebot.types.InlineKeyboardButton("🔥 پکیج کامل ۴ درس - 1,250,000 تومان", callback_data="cash_full"))
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
                text="💳 بخش خرید نقدی (آنی با تخفیف‌های ویژه تا جمعه ۱۷ مهر)\n\nمحصول مورد نظر خود را انتخاب کنید:",
                reply_markup=get_cash_markup()
            )
        except Exception as e:
            print(f"Edit cash menu error: {e}")
            
    elif call.data == "mode_installment":
        if call.from_user.id not in user_phones:
            contact_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            contact_markup.add(telebot.types.KeyboardButton("📱 اشتراک‌گذاری شماره تلفن برای خرید اقساطی", request_contact=True))
            
            try:
                bot.send_message(
                    call.message.chat.id,
                    "برای ثبت‌نام در طرح فروش اقساطی پکیج کامل، لطفاً روی دکمه زیر بزنید تا شماره تلفن شما جهت پیگیری اقساط ثبت شود:",
                    reply_markup=contact_markup
                )
            except Exception as e:
                print(f"Request phone error: {e}")
        else:
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=(
                        "🤝 بخش خرید اقساطی ویژه (فقط پکیج کامل تا ۱۷ مهر)\n\n"
                        "💰 قیمت کل: ۱,۶۰۰,۰۰۰ تومان\n"
                        "📋 شرایط پرداخت: قسط اول ۶۰۰,۰۰۰ تومان (همین الان) + دو قسط بعدی هر کدام ۵۰۰,۰۰۰ تومان (دو ماه بعد، هر ماه یک قسط)\n\n"
                        "محصول خود را انتخاب کنید:"
                    ),
                    reply_markup=get_installment_markup()
                )
            except Exception as e:
                print(f"Edit inst menu error: {e}")
                
    elif call.data == "back_to_main":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="سلام! به منوی اصلی برگشتیم. لطفاً نوع خرید خود را انتخاب کنید:",
                reply_markup=get_main_menu_markup()
            )
        except Exception as e:
            print(f"Back main error: {e}")

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
                    "🤝 بخش خرید اقساطی ویژه (فقط پکیج کامل تا ۱۷ مهر)\n\n"
                    "💰 قیمت کل: ۱,۶۰۰,۰۰۰ تومان\n"
                    "📋 شرایط پرداخت: قسط اول ۶۰۰,۰۰۰ تومان (همین الان) + دو قسط بعدی هر کدام ۵۰۰,۰۰۰ تومان\n\n"
                    "محصول خود را انتخاب کنید:"
                ),
                reply_markup=get_installment_markup()
            )
        except Exception as e:
            print(f"Contact handler error: {e}")

@bot.callback_query_handler(func=lambda call: call.data in cash_prices or call.data in installment_prices)
def handle_buy_callback(call):
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass
    
    user_id = call.from_user.id
    
    if call.data in cash_prices:
        item_name, price = cash_prices[call.data]
        user_selected_product[user_id] = f"{item_name} (نقدی)"
        text = (
            f"🛒 خرید نقدی: {item_name}\n\n"
            f"💵 مبلغ قابل پرداخت: {price} تومان\n\n"
            "💳 شماره کارت: 5022291535771289 به نام سیدحمیدرضامحسنی راد\n\n"
            "📷 لطفاً وجه را واریز کرده و عکس فیش را همینجا ارسال کنید."
        )
    else:
        item_name, price_info = installment_prices[call.data]
        user_selected_product[user_id] = f"{item_name} (اقساطی)"
        phone = user_phones.get(user_id, "ثبت نشده")
        text = (
            f"🛒 خرید اقساطی: {item_name}\n\n"
            f"📋 شرایط پرداخت: {price_info}\n"
            f"📱 شماره تماس شما: {phone}\n\n"
            "💳 شماره کارت برای واریز قسط اول: 5022291535771289 به نام سیدحمیدرضامحسنی راد\n\n"
            "📷 لطفاً قسط اول را واریز کرده و عکس فیش آن را همینجا ارسال کنید."
        )
        
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            text=text
        )
    except Exception as e:
        print(f"Edit buy text error: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def handle_approve_callback(call):
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass
        
    if call.from_user.id not in ADMIN_IDS:
        try:
            bot.answer_callback_query(call.id, "شما دسترسی ادمین ندارید!", show_alert=True)
        except:
            pass
        return
        
    user_id = int(call.data.split("_")[1])
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    try:
        bot.send_message(
            user_id, 
            "✅ فیش واریزی شما تایید شد! برای دریافت لینک دسترسی با پشتیبانی در ارتباط باشید:", 
            reply_markup=user_markup
        )
    except Exception as e:
        print(f"User send error: {e}")
    
    try:
        bot.edit_message_caption(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id,
