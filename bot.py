@bot.message_handler(func=lambda message: message.text in [
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
            bot.send_message(
                message.chat.id,
                description_text,
                reply_markup=get_main_menu_markup()
            )
    except Exception as e:
        print(f"Persistent button error: {e}")

# این هندلر متن‌های معمولی (غیر از دکمه‌ها و دستورات) رو هندل می‌کنه
@bot.message_handler(func=lambda message: True)
def handle_text_fallback(message):
    user_markup = telebot.types.InlineKeyboardMarkup()
    user_markup.add(telebot.types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    try:
        bot.send_message(
            message.chat.id,
            "لطفاً برای ارسال فیش واریزی، فقط عکس یا اسکرین‌شات فیش را ارسال کنید.",
            reply_markup=user_markup
        )
    except Exception as e:
        print(f"Fallback error: {e}")

if name == "main":
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(3)
