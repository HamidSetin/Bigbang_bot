import telebot
import time

# توکن ربات شما
TOKEN = '8604260086:AAGMYdYkNvY-sIz7dZlqjJS0Nw15AoNd__4'
bot = telebot.TeleBot(TOKEN)

# پاکسازی کامل آپدیت‌های معلق برای جلوگیری صددرصدی از ارور Conflict 409
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

# قیمت‌های بخش نقدی (تخفیف‌دار تا جمعه ۱۷ مهر ماه)
cash_prices = {
    "cash_zist": ("بانک تست زیست جامع (نقدی)", "400,000"),
    "cash_shimi": ("بانک تست شیمی جامع (نقدی)", "360,000"),
    "cash_fizik": ("بانک تست فیزیک جامع (نقدی)", "330,000"),
    "cash_math": ("بانک تست ریاضی جامع (نقدی)", "360,000"),
    "cash_full": ("پکیج کامل هر ۴ بانک تست (نقدی)", "1,250,000")
}

# قیمت و شرایط بخش اقساطی (فقط پکیج کامل - سه قسط ۶۰۰ تومانی)
installment_prices = {
    "inst_full": ("پکیج کامل هر ۴ بانک تست (اقساطی)", "600,000 تومان (قسط اول از کل ۱,۸۰۰,۰۰۰ تومان)")
}

# ذخیره موقت اطلاعات کاربران
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
    markup.row(telebot.types.InlineKeyboardButton("📦 پکیج کامل اقساطی (۳ قسط ۶۰۰ تومانی)", callback_data="inst_full"))
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
        # بررسی ثبت بودن شماره تلفن کاربر
        if call.from_user.id not in user_phones:
            contact_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            contact_markup.add(telebot.types.KeyboardButton("📞 اشتراک‌گذاری شماره تلفن برای خرید اقساطی", request_contact=True))
            
            try:
                bot.send_message(
                    call.message.chat.id,
                    "📌 برای ثبت‌نام در طرح **فروش اقساطی پکیج کامل**، لطفاً روی دکمه زیر بزنید تا شماره تلفن شما جهت پیگیری اقساط ثبت شود:",
                    reply_markup=contact_markup
                )
            except Exception as e:
                print(f"Request phone error: {e}")
        else:
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="📅 **بخش خرید اقساطی ویژه (فقط پکیج کامل)**\n\n"
                         "🔹 قیمت کل: ۱,۸۰۰,۰۰۰ تومان\n"
                         "🔹 شرایط پرداخت: ۳ قسط ۶۰۰,۰۰۰ تومانی (قسط اول همین حالا، دو قسط بعدی هر ماه سر تایم)\n\n"
                         "محصول خود را انتخاب کنید:",
                    reply_markup=get_installment_markup(),
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Edit inst menu error: {e}")
                
    elif call.data == "back_to_main":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="سلام! به منوی اصلی برگشتیم. لطفاً نوع خرید خود را انتخاب کنید:",
                reply_markup=get_main_menu_markup(),
                parse_mode="Markdown"
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
                f"✅ شماره تلفن شما (`{message.contact.phone_number}`) با موفقیت ثبت شد.",
                reply_markup=get_persistent_keyboard(),
                parse_mode="Markdown"
            )
            bot.send_message(
                message.chat.id,
                "📅 **بخش خرید اقساطی ویژه (فقط پکیج کامل)**\n\n"
                "🔹 قیمت کل: ۱,۸۰۰,۰۰۰ تومان\n"
                "🔹 شرایط پرداخت: ۳ قسط ۶۰۰,۰۰۰ تومانی (قسط اول همین حالا، دو قسط بعدی هر ماه سر تایم)\n\n"
                "محصول خود را انتخاب کنید:",
                reply_markup=get_installment_markup(),
                parse_mode="Markdown"
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
            f"💳 خرید نقدی: {item_name}\n\n"
            f"💰 مبلغ قابل پرداخت: {price} تومان\n\n"
            f"شماره کارت: `5022291535771289` به نام سیدحمیدرضامحسنی راد\n\n"
            "لطفاً وجه را واریز کرده و عکس فیش را همینجا ارسال کنید."
        )
    else:
        item_name, price_info = installment_prices[call.data]
        user_selected_product[user_id] = f"{item_name} (اقساطی)"
        phone = user_phones.get(user_id, "ثبت نشده")
        text = (
            f"📅 خرید اقساطی: {item_name}\n\n"
            f"📋 شرایط پرداخت: قسط اول {price_info}\n"
            f"📱 شماره تماس شما: `{phone}`\n\n"
            f"شماره کارت برای واریز قسط اول: `5022291535771289` به نام سیدحمیدرضامحسنی راد\n\n"
            "لطفاً قسط اول را واریز کرده و عکس فیش آن را همینجا ارسال کنید تا ادمین بررسی و تأیید کند."
        )
        
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            text=text, 
            parse_mode="Markdown"
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
    phone = user_phones.get(user_id, "ثبت نشده / ارسال نشده")
    
    markup = telebot.types.InlineKeyboardMarkup()
    if username:
        markup.add(telebot.types.InlineKeyboardButton("💬 چت مستقیم با کاربر", url=f"https://t.me/{username}"))
    markup.add(telebot.types.InlineKeyboardButton("✅ تایید فیش (بررسی شد)", callback_data=f"approve_{user_id}"))
    
    caption = (
        f"📩 فیش واریزی جدید!\n\n"
        f"📦 محصول: {product_purchased}\n"
        f"👤 نام: {user_name}\n"
        f"🔗 آیدی: {chat_info}\n"
        f"📱 شماره تماس: `{phone}`\n"
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
    
    try:
        bot.send_message(
            message.chat.id, 
            f"✅ فیش شما برای **{product_purchased}** دریافت شد.\nپس از بررسی توسط مدیریت، دسترسی ارسال خواهد شد.",
            reply_markup=user_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"User receipt ack error: {e}")

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
    
    try:
        if message.text == "🚀 منوی اصلی / شروع":
            bot.send_message(
                message.chat.id,
                "سلام دوباره! به منوی اصلی برگشتیم. لطفاً نوع خرید خود را انتخاب کنید:",
                reply_markup=get_main_menu_markup()
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
                "👇 همین الان نوع خرید خود را انتخاب کنید:",
                reply_markup=user_markup
            )
    except Exception as e:
        print(f"Persistent button error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_text_fallback(message):
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    try:
        bot.send_message(
            message.chat.id,
            "⚠️ لطفاً برای ارسال فیش واریزی، **فقط عکس یا اسکرین‌شات فیش** را ارسال کنید.",
            reply_markup=user_markup
        )
    except Exception as e:
        print(f"Fallback error: {e}")

# حلقه امن پولینگ
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=30)
    except Exception as e:
        print(f"Polling Error: {e}")
        time.sleep(3)
