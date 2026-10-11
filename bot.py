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
                    "🤝 بخش خرید اقساطی ویژه (فقط پکیج کامل )\n\n"
                    "💰 قیمت کل: 1,800,000 تومان\n"
                    "📋 شرایط پرداخت: قسط اول 600,000 تومان (همین الان) + دو قسط بعدی هر کدام 600,000 تومان\n\n"
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
        bot.answer_callback_query(call.id)
    except Exception:
        pass
    
    if call.data == "mode_cash":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="💳 بخش خرید نقدی (آنی با تخفیف‌های ویژه تا )\n\nمحصول مورد نظر خود را انتخاب کنید:",
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
                        "🤝 بخش خرید اقساطی ویژه (فقط پکیج کامل)\n\n"
                        "💰 قیمت کل: 1,800,000 تومان\n"
                        "📋 شرایط پرداخت: قسط اول 600,000 تومان (همین الان) + دو قسط بعدی هر کدام 600,000 تومان (دو ماه بعد، هر ماه یک قسط)\n\n"
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
            caption=call.message.caption + "\n\n🟢 وضعیت: تایید شد توسط ادمین"
        )
    except Exception as e:
        print(f"Caption edit error: {e}")
        if name == "main":
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(3)
