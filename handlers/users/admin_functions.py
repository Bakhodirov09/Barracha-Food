from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove

from loader import types, dp, admins, user_settings, menu, _, other
from all_keyboards import admin_keyboards, user_keyboards
from aiogram.dispatcher import FSMContext


@dp.message_handler(state='admin_state')
async def admin_functions_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text[0] == "🍴":
        await message.answer(text=message.text, reply_markup=await admin_keyboards.menu_settings(lang=user['lang']))
        await state.set_state('in_menu_settings')
    elif message.text.split(' ')[0] == "✍️":
        await message.answer(
            text=_(f"😊 Foydalanuvchilarga yubormoqchi bolgan xabaringiz uchun rasm yoki video yuboring.", locale=user['lang']),
            reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('get_photo_or_video_for_message')
    elif message.text[0] == "🏷":
        await message.answer(text=_(f"🏷 Aksiya sozlamalari", locale=user['lang']),
                             reply_markup=await admin_keyboards.stock_settings(lang=user['lang']))
        await state.set_state('in_stock_settings')
    elif message.text[0] == "📍":
        await message.answer(text=message.text, reply_markup=await admin_keyboards.filial_settings(lang=user['lang']))
        await state.set_state('in_filial_settings')
    elif message.text[0] == "👥":
        chat_id = message.chat.id
        user = await user_settings.get_user(chat_id=chat_id)
        userss = _("😊 Barcha foydalanuvchilar", locale=user['lang'])
        users = _("📰 Foydalanuvchilar ro'yxati: \n\nId  | Til \t\t | Ism Familya   | Username       |\n",
                  locale=user['lang'])

        count = 0
        all_users = await user_settings.get_all_users()

        for i in all_users:
            lang = "🇺🇿" if i['lang'] == "uz" else "🇷🇺"
            full_name = i['full_name'] if len(i['full_name']) <= 10 else i['full_name'][:10] + "..."

            if i['username'].startswith('@'):
                username = f"<a href='https://t.me/{i['username'][1:]}'>Foydalanuvchi</a>"
            else:
                username = f"<a href='tg://user?id={i['chat_id']}'>Foydalanuvchi</a>"

            users += f"{str(i['id']):<3} | {lang} | {full_name:<12} | {username:<14} |\n"
            count += 1

        users += _(f"\n👥 Ja'mi foydalanuvchilar: ", locale=user['lang'])
        users += f"<b>{count}</b>"

        await message.answer(text=userss, reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await message.answer(text=users, reply_markup=await admin_keyboards.admin_user_settings(lang=user['lang']),
                             parse_mode='HTML', disable_web_page_preview=True)
        await state.set_state('admin_state')
    elif message.text[0] == "👤":
        await message.answer(text=message.text, reply_markup=await admin_keyboards.admins(lang=user['lang']))
        await state.set_state('admin_in_admin_settings')
    elif message.text[0] == "🌐":
        await message.answer(text=message.text, reply_markup=await admin_keyboards.socials(lang=user['lang']))
        await state.set_state('admin_in_socials')
    elif message.text[0] == "🔁":
        await message.answer(text=_(f"😊 Yangi logono yuboring", locale=user['lang']),
                             reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_new_logo')
    elif message.text[0] == "🍽":
        logo = await other.get_logo()
        menu_btn = InlineKeyboardMarkup(row_width=2)
        menu_btn.insert(InlineKeyboardButton(text=_(f"⬅️ Ortga", locale=user['lang']), callback_data='back_to_main_menu'))
        menu_btn.insert(InlineKeyboardButton(text=_(f"🛍 Savat", locale=user['lang']), callback_data='basket'))
        stock_status = await other.get_stock_status()
        if stock_status:
            menu_btn.insert(InlineKeyboardButton(text=_(f"🎉 Aksiya", locale=user['lang']), callback_data=f"{stock_status['name']}_{stock_status['id']}"))
        for menyu in await menu.get_menu(lang=user['lang']):
            if menyu['name_to_get'] != 'Aksiya':
                menu_btn.insert(InlineKeyboardButton(text=menyu['name'], callback_data=f"{menyu['name']}_{menyu['id']}"))
        await message.answer(text=_(f"😋 Bizning menyu", locale=user['lang']),
                             reply_markup=await user_keyboards.main_menu_basket(lang=user['lang']))
        await message.answer_photo(photo=logo['photo'], reply_markup=menu_btn)
        await state.set_state('in_menu')

@dp.message_handler(state='in_filial_settings')
async def in_filial_settings_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    filials_message = "📍 Barcha filial\n\n"
    count = 0
    for filial in await other.get_all_filials(lang=user['lang']):
        filials_message += f"{filial['id']} | {filial['name']}"
        count += 1
    filials_message += f"Ja'mi filiallar: {count} ta"
    if message.text.split(' ')[0] == "➕📍":
        await message.answer(text=_(f"📍 Yangi filial qayerda joylashgan?\nMasalan: Sergeli", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_new_filial_name')
    elif message.text.split(' ')[0] == "🚫📍":
        await message.answer(text=_(f"🆔 O'chirmoqchi bo'lgan filial id raqamini kiriting.", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_id_to_delete_filial')
    elif message.text.split(' ')[0] == "":
        pass

@dp.message_handler(state='send_id_to_delete_filial')
async def send_id_to_delete_filial_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await other.delete_filial(id=int(message.text))
        await message.answer(text=_(f"✅ Filial ochirildi", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except:
        await message.answer(text=_(f"😕 Kechirasiz bro siz id raqam noto'g'ri kiritdingiz. Yoki bunday id raqamli filial mavjud emas!", locale=user['lang']))

@dp.message_handler(state='send_new_filial_name')
async def send_new_filial_name_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'name': message.text
    })
    await message.answer(text=_(f"📍 Yangi filial joylashuvini yuboring.", locale=user['lang']), reply_markup=await user_keyboards.send_location(lang=user['lang']))
    await state.set_state('send_new_filial_location')

@dp.message_handler(state='send_new_filial_location', content_types=types.ContentType.LOCATION)
async def send_new_filial_location_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'latitude': message.location.latitude,
        'longitude': message.location.longitude
    })
    await message.answer(text=_(f"🖼 Yangi filial rasmini yuboring.", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
    await state.set_state('send_new_filial_photo')

@dp.message_handler(state='send_new_filial_photo', content_types=types.ContentType.PHOTO)
async def send_new_filial_photo_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'photo': message.photo[-1].file_id
    })
    data = await state.get_data()
    await other.add_filial(data=data)
    await message.answer(text=_(f"✅ Yangi filial qo'shildi", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
    await state.set_state('admin_state')

@dp.message_handler(state='admin_in_socials')
async def admin_in_socials_handlers(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    userga = _(f"🌐 Ijtimoiy tarmoqlar\n\n")
    for social in await other.get_all_socials():
        userga += f"{social['id']} | <a href='{social['link']}'>{social['name']}</a>"
    await message.answer(text=userga, reply_markup=await user_keyboards.users_panel(lang=user['lang']))
    if message.text.split(' ')[0] == "➕🌐":
        await message.answer(text=_(f"🌐 Yangi ijtimoiy tarmoq qaysi dasturda joylashgan?\nMasalan: YouTube", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_new_social_name')
    elif message.text.split(' ')[0] == "🚫🌐":
        await message.answer(text=_(f"🌐 Qaysi ijtimoiy tarmoqni olib tashlamoqchisiz? ID Raqamini kiriting", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_remove_social_id')
    elif message.text.split(' ')[0] == "🌐":
        pass

@dp.message_handler(state='send_new_social_name')
async def send_new_social_name_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'name': message.text
    })
    await message.answer(text=_(f"🔗 Yangi ijtimoiy tarmoq linkini yuboring.", locale=user['lang']))
    await state.set_state('send_new_social_link')

@dp.message_handler(state='send_new_social_link')
async def send_new_social_link_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'link': message.text
    })
    data = await state.get_data()
    await other.add_social(data=data)
    await message.answer(text=_(f"✅ Yangi ijtimoiy tarmoq qoshildi.", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
    await state.set_state('admin_state')

@dp.message_handler(state='send_remove_social_id')
async def send_remove_social_id_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await other.delete_social(id=int(message.text))
        await message.answer(text=_(f"✅ Ijtimoiy tarmoq ochirib yuborildi", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except:
        await message.answer(text=_(f"😕 Kechrasiz bro. Bunday id raqamli IJtimoiy tarmoq mavjud emas, yoki siz id raqamni no'tog'ri kiritdigiz.", locale=user['lang']))

@dp.message_handler(state='admin_in_admin_settings')
async def admin_in_admin_settings_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    admins_list = await admins.get_all_admins()
    admins_message = _("📰 Adminlar ro'yxati:\n\n", locale=user['lang'])
    count = 0
    for admin in admins_list:
        about_admin = await user_settings.get_user(chat_id=admin['chat_id'])
        admins_message += f"{admin['id']} | {about_admin['full_name']}\n"
        count += 1
    admins_message += f"\n👥 Ja'mi adminlar: {count}"
    if message.text.split(' ')[0] == "➕👤":
        await message.answer(text=_(f"✍️ Yangi admin chat id raqamini yozing", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_new_admin_chat_id')
    elif message.text.split(' ')[0] == "🚫👤":
        await message.answer(text=admins_message)
        await message.answer(text=_(f"✍️ Olib tashlamoqchi bo'lgan adminingiz id raqamini kiriting.", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_id_to_remove_admin')
    elif message.text.split(' ')[0] == "👤":
        await message.answer(text=admins_message)

@dp.message_handler(state='send_id_to_remove_admin')
async def send_id_to_remove_admin_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    admin = await admins.get_admin(id=int(message.text))
    if admin:
        await admins.delete_admin(id=int(message.text))
        try:
            await dp.bot.send_message(chat_id=admin['chat_id'], text="😕 Kechirasiz bro. Siz bizning botimizda boshqa adminlar tomonidan, adminlar bo'limidan ochirib yuborildingiz. Qayta /start bosib botni ishlatishingiz mumkin.!", reply_markup=ReplyKeyboardRemove())
        except:
            pass
        await message.answer(text=_(f"✅ Adminlar qatoridan ochirib yuborildi", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
    else:
        await message.answer(text=_(f"😕 Kechirasiz bro. Siz id raqamni noto'gri kiritdingiz. Yoki agar to'gri kiritgan bo'lsangiz admin ochirib yuborilganini '👤 Adminlar' bo'limidagi '👤 Adminlar' funksiyasi orqali yana 1 tekshirib ko'ring!:)", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
    await state.set_state('admin_state')

@dp.message_handler(state='send_new_admin_chat_id')
async def send_new_admin_chat_id_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        admin = await user_settings.get_user(chat_id=int(message.text))
        adminga = _(f"😉 Tabriklaymiz ", admin['lang'])
        adminga += f"\n {admin['full_name']} "
        adminga += _(f"siz bizning Barracha Food botimizda adminlik huquqiga ega bo'ldingiz. Adminlik huquqidan foydalanishingiz mumkin!")
        await dp.bot.send_message(chat_id=int(message.text), text=adminga, reply_markup=await admin_keyboards.admins_panel(lang=admin['lang']))
        await admins.add_admin(chat_id=int(message.text))
        await message.answer(text=_(f"✅ Yangi admin qoshildi.", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except:
        await message.answer(text=_(f"❌ Kechirasiz bro. Siz chat id raqamni noto'g'ri kiritdingiz, yoki bunday chat id raqamli foydalanuvchi mavjud emas! Tekshirib qayta kiritishingiz mumkin! 😉", locale=user['lang']))

@dp.message_handler(state='in_stock_settings')
async def in_stock_settings_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text.split(' ')[0] == "🏷":
        if await other.get_stock_status():
            await message.answer(text=_(f"‼️ Aksiya hozirda aktiv holatda. Aksiyani ochirasizmi?", locale=user['lang']), reply_markup=await user_keyboards.accept(lang=user['lang']))
            await state.set_state('are_you_accept_deactivate_stock')
        else:
            await message.answer(text=_(f"‼️ Aksiya hozirda aktiv bolmagan holatda. Aksiyani aktivlashtirasizmi?", locale=user['lang']), reply_markup=await user_keyboards.accept(lang=user['lang']))
            await state.set_state('are_you_accept_activate_stock')
    elif message.text.split(' ')[0] == "➕🏷":
        await message.answer(text=_(f"✍️ Aksiya uchun yangi taom nomini uzbek tilida kiriting.", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_new_stock_food_name')

@dp.message_handler(state='send_new_stock_food_name')
async def send_new_stock_food_name_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'name_uz': message.text
    })
    await message.answer(text=_(f"✍️ Aksiya uchun taom nomini endi rus tilida kiritng", locale=user['lang']))
    await state.set_state('send_new_stock_food_name_ru')

@dp.message_handler(state='send_new_stock_food_name_ru')
async def send_new_stock_food_name_ru_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'name_ru': message.text
    })
    await message.answer(text=_(f"🖼 Aksiyadagi taom uchun rasm kiriting.", locale=user['lang']))
    await state.set_state('send_photo_for_stock_food')

@dp.message_handler(state='send_photo_for_stock_food', content_types=types.ContentType.PHOTO)
async def send_photo_for_stock_food_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'photo': message.photo[-1].file_id
    })
    await message.answer(text=_(f"✍️ Aksiyadagi taom uchun ma'lumot qo'shing, Uzbek tilida", locale=user['lang']))
    await state.set_state('send_stock_description_uz')

@dp.message_handler(state='send_stock_description_uz')
async def send_stock_description_uz_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'desc_uz': message.text
    })
    await message.answer(text=_(f"✍️ Aksiyadagi taom ma'lumotini endi rus tilida kiriting", locale=user['lang']))
    await state.set_state('send_stock_product_desc_ru')

@dp.message_handler(state='send_stock_product_desc_ru')
async def send_stock_product_desc_ru_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'desc_ru': message.text
    })
    await message.answer(text=_(f"✍️ Aksiyadagi taom narxini kiriting.\nButun sonlarda", locale=user['lang']))
    await state.set_state('send_stock_product_price')

@dp.message_handler(state='send_stock_product_price')
async def send_stock_product_price_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await state.update_data({
            'price': int(message.text)
        })
        data = await state.get_data()
        await other.add_stock_product(data=data)
        await message.answer(text=_(f"✅ Aksiya uchun yangi taom qoshildi", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except:
        pass

@dp.message_handler(state='are_you_accept_deactivate_stock')
async def are_you_accept_deactivate_stock_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text.split(' ')[0] == "✅":
        await message.answer(_(f"✅ Aksiya holati ochirildi.", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
    else:
        await message.answer(text=_(f"✅ Aksiya holati aktiv holatda turibdi!", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
    await state.set_state('admin_state')

@dp.message_handler(state='are_you_accept_activate_stock')
async def are_you_accept_activate_stock_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text.split(' ')[0] == "✅":
        await message.answer(_(f"🖼 Aksiya holatini aktivlashtirish uchun aksiya rasmini yuboring.", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('send_new_stock_photo')
    else:
        await message.answer(text=_(f"✅ Aksiya holati aktiv bo'lmagan holatda turibdi!", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')

@dp.message_handler(state='send_new_stock_photo', content_types=types.ContentType.PHOTO)
async def are_you_accept_activate_stock_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await other.update_stock_status_true(photo=message.photo[-1].file_id)
    await message.answer(text=_(f"🥳 Yangi aksiya qoshildi. Aksiyaga taomlar qoshishingiz mumkin.", locale=user['lang']), reply_markup=await admin_keyboards.stock_settings(lang=user['lang']))
    await state.set_state('in_stock_settings')


@dp.message_handler(state='get_photo_or_video_for_message', content_types=[types.ContentType.VIDEO, types.ContentType.PHOTO])
async def get_photo_or_vide_for_message_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    title = _(f"Foydalanuvchilarga yubormoqchi bo'lgan xabaringizni kirtiting.", locale=user['lang'])
    if message.video:
        await state.update_data({
            'video': message.video.file_id
        })
        await message.answer(text=title)
        await state.set_state('send_message_to_users')
    elif message.photo:
        await state.update_data({
            'photo': message.photo[-1].file_id
        })
        await message.answer(text=title)
        await state.set_state('send_message_to_users')
    else:
        await message.answer(text=_(f"Kechirasiz bro. Rasm yoki videoni 1 dona yuboring", locale=user['lang']))
        await state.set_state('get_photo_or_video_for_message')

@dp.message_handler(state='send_message_to_users', content_types=types.ContentType.TEXT)
async def send_message_to_users_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'title': message.text
    })
    data = await state.get_data()
    user = await user_settings.get_user(chat_id=message.chat.id)
    all_users = await user_settings.get_all_users()
    adminga = _(f"✉️ Foydalanuvchilarga xabar yuborilmoqda ⏳", locale=user['lang'])
    await message.answer(text=adminga, reply_markup=ReplyKeyboardRemove())

    for user in all_users:
        try:
            if data.get('video', None):
                await dp.bot.send_video(chat_id=user['chat_id'], video=data['video'], caption=data['title'])
            else:
                await dp.bot.send_photo(chat_id=user['chat_id'], photo=data['photo'], caption=data['title'])
        except Exception as e:
            pass

    await message.answer(text=_(f"✅ Foydalanuvchilarga xabar yuborildi", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
    await state.set_state('admin_state')


@dp.callback_query_handler(state='admin_state', text='delete_user')
async def send_id_to_delete_user_handler(call: types.CallbackQuery, state: FSMContext):
    user = await user_settings.get_user(chat_id=call.message.chat.id)
    await call.message.answer(text=_(f"✍️ Ochirmoqchi bo'lgan foydalanuvchi id raqamini kiriting", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
    await state.set_state('send_id_to_delete_user')

@dp.callback_query_handler(state='admin_state', text='block_user')
async def send_id_to_delete_user_handler(call: types.CallbackQuery, state: FSMContext):
    user = await user_settings.get_user(chat_id=call.message.chat.id)
    await call.message.answer(text=_(f"✍️ Bloklamoqchi bo'lgan foydalanuvchi id raqamini kiriting", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
    await state.set_state('send_id_to_block_user')

@dp.message_handler(state='send_id_to_block_user')
async def send_id_to_block_user_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await state.update_data({
            "id": int(message.text)
        })
        await message.answer(text=_(f"🕔 Ushbu foydalanuvchini necha kunga blok qilmoqchisiz?", locale=user['lang']))
        await state.set_state('how_many_times')
    except Exception as e:
        print(e)
        await message.answer(text=_(f"😕 Kechirasiz bro siz id raqam no'tog'ri kiritdingiz yoki bunday id raqamli foydalanuvchi mavjud emas!‼️",locale=user['lang']))
        await state.set_state('send_id_to_block_user')

@dp.message_handler(state='how_many_times')
async def how_many_times_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await state.update_data({
            'day': int(message.text)
        })
        data = await state.get_data()
        await admins.block_user(data=data, date=message.date)
        adminga = _(f"✅ Foydalanuvchi ", locale=user['lang'])
        adminga += message.text
        adminga += _(f" kunga bloklandi.", locale=user['lang'])
        await message.answer(text=adminga, reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
    except Exception as e:
        print(e)
        await message.answer(text=_(f"😕 Kechirasiz bro. Siz bloklamoqchi bo'lgan foydalanuvchi id raqamini yoki vaqtni to'gri kiritmadingiz. Qayta urinib korishingiz mumkin.", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')

@dp.message_handler(state='send_id_to_delete_user')
async def delete_user_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(message.chat.id)
    try:
        await admins.delete_user(pk=int(message.text))
        await message.answer(text=_(f"✅ Foydalanuvchi muvaffaqqiyatli ochirib yuborildi", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except Exception as e:
        await message.answer(text=_(f"😕 Kechirasiz bro siz id raqam no'tog'ri kiritdingiz yoki bunday id raqamli foydalanuvchi mavjud emas!‼️", locale=user['lang']))
        await state.set_state('send_id_to_delete_user')
@dp.message_handler(state='in_menu_settings')
async def in_menu_settings_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    all_menu = await menu.get_menu(lang=user['lang'])
    menu_btn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    menu_btn.insert(KeyboardButton(text=_(f"❌ Bekor qilish", locale=user['lang'])))
    for i in all_menu:
        menu_btn.insert(KeyboardButton(text=i['name']))
        menu_btn.row_width = 2
    if message.text[0:2] == "➕🍴":
        await message.reply(text=_(f"😊 Yangi menyu nomini uzbek tilida kiriting.", locale=user['lang']),
                            reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('get_new_menu_name_uz')
    elif message.text[0:2] == "🚫🍴":
        await message.reply(text=_(f"😊 Ochirmoqchi bo'lgan menyuingizni tanlang.", locale=user['lang']),
                            reply_markup=menu_btn)
        await state.set_state('select_menu_for_delete')
    elif message.text[0:2] == "➕🌯":
        await message.reply(text=_(f"😊 Yangi taomni qaysi menyuga qoshmoqchisiz?", locale=user['lang']),
                            reply_markup=menu_btn)
        await state.set_state('select_menu_to_add_food')
    elif message.text[0:2] == "🚫🌯":
        await message.reply(
            text=_(f"😊 Olib tashlamoqchi bo'lgan taomingiz qaysi menyuda joylashgan?", locale=user['lang']),
            reply_markup=menu_btn)
        await state.set_state('select_menu_to_delete_food')
    elif message.text[0:2] == "🔧💰":
        await message.reply(
            text=_(f"😊 Narxini ozgartirmoqchi bo'lgan taomingiz qaysi menyuda joylashgan?", locale=user['lang']),
            reply_markup=menu_btn)
        await state.set_state('select_menu_to_change_food_price')
    elif message.text[0:2] == "🔧🖼":
        await message.reply(
            text=_(f"😊 Rasmini ozgartirmoqchi bo'lgan taomingiz qaysi menyuda joylashgan?", locale=user['lang']),
            reply_markup=menu_btn)
        await state.set_state('select_menu_to_change_food_photo')
    else:
        await message.reply(text=_(f"😕 Funksiya topilmadi", locale=user['lang']),
                            reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')


@dp.message_handler(state='send_new_logo', content_types=types.ContentType.PHOTO)
async def send_new_logo_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await other.update_logo(photo=message.photo[-1].file_id)
        await message.answer(text=_(f"✅ Logo muvaffaqqiyatli o'zgartirildi", locale=user['lang']),
                             reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except Exception as e:
        print(e)


@dp.message_handler(state='select_menu_to_change_food_photo')
async def select_menu_to_change_food_photo_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        menu_id = await menu.get_menu_with_name(menu_name=message.text, lang=user['lang'])
        await state.update_data({
            'menu_id': menu_id['id']
        })
        menu_foods = await menu.get_menu_foods(menu_id=menu_id['id'], lang=user['lang'])
        menu_foods_btn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        menu_foods_btn.insert(KeyboardButton(text=_(f"❌ Bekor qilish", locale=user['lang'])))
        for food in menu_foods:
            menu_foods_btn.insert(KeyboardButton(text=food['name']))
            menu_foods_btn.row_width = 2
        await message.answer(text=_(f"😊 Qaysi taomning rasmini o'zgartirmoqchisiz?", locale=user['lang']), reply_markup=menu_foods_btn)
        await state.set_state('select_food_to_change_photo')
    except Exception as e:
        print(e)

@dp.message_handler(state='select_food_to_change_photo')
async def select_food_to_change_photo_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'name': message.text
    })
    await message.answer(text=_(f"😊 Ushbu taom uchun yangi surat yuboring.",locale=user['lang']))
    await state.set_state('send_photo_to_change_food_photo')

@dp.message_handler(state='send_photo_to_change_food_photo', content_types=types.ContentType.PHOTO)
async def send_photo_to_change_food_photo_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await state.update_data({
            'photo': message.photo[-1].file_id
        })
        data = await state.get_data()
        await menu.change_food_photo(data=data)
        await message.answer(text=_(f"🥳 Taom rasmi muvaffaqqiyatli o'zgartirildi.", locale=user['lang']), reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except Exception as e:
        print(e)

@dp.message_handler(state='select_menu_to_change_food_price')
async def select_menu_to_change_food_price_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        menuu = await menu.get_menu_with_name(menu_name=message.text, lang=user['lang'])
        await state.update_data({
            'menu_id': menuu['id']
        })
        menu_foods = await menu.get_menu_foods(menu_id=menuu['id'], lang=user['lang'])
        menu_foods_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        menu_foods_btn.insert(KeyboardButton(text=_(f"❌ Bekor qilish", locale=user['lang'])))
        for food in menu_foods:
            menu_foods_btn.insert(KeyboardButton(text=food['name']))
            menu_foods_btn.row_width = 2
        await message.answer(text=_(f"😊 Narxini o'zgartirmoqchi bo'lgan taomingizni tanlang.", locale=user['lang']),
                             reply_markup=menu_foods_btn)
        await state.set_state('select_food_to_change_price')
    except Exception as e:
        print(e)


@dp.message_handler(state='select_food_to_change_price')
async def select_food_to_change_price_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'name': message.text
    })
    await message.answer(text=_(f"✍️ Ushbu taom uchun yangi narx kiriting.\n‼️ Butun sonlarda ‼️"),
                         reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
    await state.set_state('write_food_price_to_update')


@dp.message_handler(state='write_food_price_to_update')
async def write_food_price_to_update_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await state.update_data({
            'new_price': int(message.text)
        })
        data = await state.get_data()
        await menu.change_food_price(data=data)
        await message.answer(text=_(f"✅ Taom narxi muvaffaqqiyatli o'zgartirildi", locale=user['lang']),
                             reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except ValueError:
        await message.answer(text=_(f"‼️ Taom narxini faqat butun sonlarda kiritish mumkin ‼️", locale=user['lang']))
        await state.set_state('write_food_price_to_update')
    except Exception as e:
        print(e)


@dp.message_handler(state='select_menu_to_delete_food')
async def select_menu_to_delete_food(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        menu_id = await menu.get_menu_with_name(menu_name=message.text, lang=user['lang'])
        foods = await menu.get_menu_foods(menu_id=menu_id['id'], lang=user['lang'])
        foods_btn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        foods_btn.insert(KeyboardButton(text=_(f"❌ Bekor qilish", locale=user['lang'])))
        for food in foods:
            foods_btn.insert(KeyboardButton(text=food['name']))
            foods_btn.row_width = 2

        await state.update_data({
            'menu_id': menu_id['id']
        })
        await message.answer(text=_(f"😊 Olib tashlamoqchi bo'lgan taomingizni tanlang.", locale=user['lang']),
                             reply_markup=foods_btn)
        await state.set_state('select_food_to_delete')
    except Exception as e:
        print(e)


@dp.message_handler(state='select_food_to_delete')
async def select_food_to_delete_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await state.update_data({
            'name': message.text
        })
        data = await state.get_data()
        await menu.delete_food(data=data)
        await message.answer(text=_(f"✅ Taom muvaffaqqiyatli olib tashlandi.", locale=user['lang']),
                             reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except Exception as e:
        print(e)


@dp.message_handler(state='select_menu_to_add_food')
async def select_menu_to_add_food_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'menu': message.text,
        'lang': user['lang']
    })

    await message.answer(text=_(f"😊 Yangi taomni nomini kiriting. Uzbek tilida", locale=user['lang']),
                         reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
    await state.set_state('write_food_name_uz')


@dp.message_handler(state='write_food_name_uz')
async def write_food_name_uz_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'name_uz': message.text
    })
    await message.answer(text=_(f"😊 Yangi taom nomini endi rus tilida kiriting.", locale=user['lang']))
    await state.set_state('write_food_name_ru')


@dp.message_handler(state='write_food_name_ru')
async def write_food_name_ru_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'name_ru': message.text
    })
    await message.answer(text=_(f"😊 Yangi taom haqida ma'lumot kiriting. Uzbek tilida", locale=user['lang']))
    await state.set_state('write_new_food_desc_uz')


@dp.message_handler(state='write_new_food_desc_uz')
async def write_new_food_desc_uz_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'desc_uz': message.text
    })
    await message.answer(text=_(f"😊 Yangi taom nomini endi res tilida kiriting.", locale=user['lang']))
    await state.set_state('write_new_food_desc_ru')


@dp.message_handler(state='write_new_food_desc_ru')
async def write_new_food_desc_ru_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(message.chat.id)
    await state.update_data({
        'desc_ru': message.text
    })
    await message.answer(text=_(f"😊 Yangi taom narxini kiriting.\n‼️ Butun sonlarda ‼️", locale=user['lang']))
    await state.set_state('write_new_food_price')


@dp.message_handler(state='write_new_food_price')
async def write_new_food_price_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(message.chat.id)
    try:
        await state.update_data({
            'price': int(message.text)
        })
        await message.answer(text=_(f"😊 Yangi taom rasmini yuboring.", locale=user['lang']))
        await state.set_state('send_new_meal_photo')
    except ValueError:
        await message.answer(text=_(f"‼️Yangi taom narxini butun sonlarda kiriting.‼️", locale=user['lang']))
        await state.set_state('write_new_food_price')


@dp.message_handler(state='send_new_meal_photo', content_types=types.ContentType.PHOTO)
async def send_new_meal_photo_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            'photo': message.photo[-1].file_id
        })
        data = await state.get_data()
        await menu.add_food(data=data)
        user = await user_settings.get_user(chat_id=message.chat.id)
        await message.answer(text=_(f"🥳 Yangi taom muvaffaqqiyatli qoshildi", locale=user['lang']),
                             reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except Exception as e:
        print(e)


@dp.message_handler(state='select_menu_for_delete')
async def select_menu_for_delete_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    try:
        await menu.delete_menu(menu_name=message.text)
        await message.answer(text=_(f"✅ Menyu muvaffaqqiyatli ochirib yuborildi.", locale=user['lang']),
                             reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    except Exception as e:
        pass


@dp.message_handler(state='get_new_menu_name_uz')
async def get_new_menu_name_uz_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'uz': message.text
    })
    user = await user_settings.get_user(chat_id=message.chat.id)
    await message.answer(text=_(f"😊 Endi yangi menyu nomini ruschada kiriting.", locale=user['lang']))
    await state.set_state('get_new_menu_name_ru')


@dp.message_handler(state='get_new_menu_name_ru')
async def get_new_menu_name_ru_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'ru': message.text
    })
    user = await user_settings.get_user(message.chat.id)
    await message.answer(text=_(f"Yangi menyuni rasmini yuboring"))
    await state.set_state('send_new_menu_photo')


@dp.message_handler(state='send_new_menu_photo', content_types=types.ContentType.PHOTO)
async def send_new_menu_photo_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    await state.update_data({
        'photo': message.photo[-1].file_id
    })
    data = await state.get_data()
    try:
        await menu.add_menu(data=data)
        await message.answer(text=_(f"🥳 Yangi menyu muvaffaqqiyatli qoshildi.", locale=user['lang']),
                             reply_markup=await admin_keyboards.admins_panel(user['lang']))
        await state.set_state('admin_state')
    except Exception as e:
        print(e)
