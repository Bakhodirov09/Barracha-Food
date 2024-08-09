from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.inline.inline_keyboards import *
from loader import dp, admins, menu, user_settings, other
from loader import _
from all_keyboards import admin_keyboards, user_keyboards
from regex import check_phone_number


@dp.message_handler(state='in_start')
async def in_start_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(message.chat.id)
    logo = await other.get_logo()
    if message.text[0] == "🍴":
        menu_btn = InlineKeyboardMarkup(row_width=2)
        menu_btn.insert(InlineKeyboardButton(text=_(f"⬅️ Ortga", locale=user['lang']), callback_data='back_to_main_menu'))
        menu_btn.insert(InlineKeyboardButton(text=_(f"🛍 Savat", locale=user['lang']), callback_data='basket'))
        stock_status = await other.get_stock_status()
        stock = _(f"🎉 Aksiya", locale=user['lang'])
        if stock_status:
            menu_btn.insert(InlineKeyboardButton(text=stock, callback_data=f"{stock_status['name']}_{stock_status['id']}"))
        for menyu in await menu.get_menu(lang=user['lang']):
            if menyu['name_to_get'] != 'Aksiya':
                menu_btn.insert(InlineKeyboardButton(text=menyu['name'], callback_data=f"{menyu['name']}_{menyu['id']}"))
        await message.answer(text=_(f"😋 Bizning menyu", locale=user['lang']), reply_markup=await user_keyboards.main_menu_basket(lang=user['lang']))
        await message.answer_photo(photo=logo['photo'], reply_markup=menu_btn)
        await state.set_state('in_menu')
    elif message.text.split(' ')[0] == "🛍":
        order_numbers = await user_settings.get_order_numbers(user_id=user['id'])
        if order_numbers:
            for order in order_numbers:
                userga = ""
                history = await user_settings.get_history_buys(order['id'])
                for i in history:
                    food = await menu.get_food_with_id(food_id=i['food_id'])
                    userga += f"<b>{food['name']}</b> \t | \t {i['quantity']} \t | \t {food['price'] * i['quantity']}\n"
                userga += _(f"\n📅 Sotib olingan sana: ")
                userga += str(order['date'])
                userga += _(f"\n🚚 Buyurtma turi: ")
                userga += f"<b>{order['type']}</b>"
                if order['where_to'] is not None:
                    userga += _('\n📍 Buyurtma berilgan manzil: ')
                    userga += f"<b>{order['where_to']}</b>"
                elif order['which_filial'] != "null":
                    userga += _("\n🚶 Olib ketish uchun filial: ")
                    userga += f"<b>{order['which_filial']}</b>"
                userga += _(f"\n\n💰 Ja'mi: ")
                userga += f"<b>{order['total']}</b>"
                await message.answer(text=userga)
        else:
            await message.answer(text=_(f"😕 Kechirasiz. Siz bizning botimizdan hali hech narsa buyurtma qilmagansiz!", locale=user['lang']))
    elif message.text.split(' ')[0] == "✍️":
        await message.answer(text=_(f"😊 Izohingizni yozing", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('write_comment')
    elif message.text.split(' ')[0] == "ℹ️":
        about = await other.get_about(lang=user['lang'])
        userga = _(f"😊 Biz haqimizda: \n", locale=user['lang'])
        userga += about['about']
        await message.answer_photo(photo=logo['photo'], caption=about['about'])
        await state.set_state('in_start')
    elif message.text.split(' ')[0] == "📍🌐":
        await message.answer(text=_(f"😊 Ozingizga kerakli bo'limni tanlang.", locale=user['lang']), reply_markup=await user_keyboards.filials_and_socials(lang=user['lang']))
        await state.set_state('select_option')
    elif message.text.split(' ')[0] == "⚙️":
        await message.answer(text=_(f"⚙️ Sizning sozlamalaringiz."), reply_markup=await user_keyboards.user_settings_menu(lang=user['lang']))
        await state.set_state('in_settings')

@dp.message_handler(state='select_option')
async def select_option_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text[0] == "📍":
        filials_btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        filials_btn.insert(KeyboardButton(text=_(f"⬅️ Ortga", locale=user['lang'])))
        filials_btn.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user['lang'])))
        for filial in await other.get_all_filials(lang=user['lang']):
            filials_btn.insert(KeyboardButton(text=f"📍 {filial['name']}"))
        await message.answer(text=message.text, reply_markup=filials_btn)
        await state.set_state('in_filials')
    elif message.text[0] == "🌐":
        socials = await other.get_all_socials()
        userga = _(f"🌐 Bizning ijtimoiy tarmoqdagi sahifalarimiz. \n\n", locale=user['lang'])
        for social in socials:
            userga += f"<a href='{social['link']}'>{social['name']}</a>"
        await message.answer(text=userga, reply_markup=await user_keyboards.users_panel(lang=user['lang']))
        await state.set_state('in_start')

@dp.message_handler(state='in_filials')
async def in_filials_handler(message: types.Message, state: FSMContext):
    filial = await other.get_filial(name=message.text[2:])
    user = await user_settings.get_user(chat_id=message.chat.id)
    if filial:
        userga = _(f"📍 Filial: ", locale=user['lang'])
        userga += f"{filial['name']}\n"
        userga += _(f"🕔 Ish vaqti: 09:00 dan 03:00 gacha", locale=user['lang'])
        await message.reply_location(latitude=filial['latitude'], longitude=filial['longitude'])
        await message.reply_photo(caption=userga, photo=filial['photo'], reply_markup=await user_keyboards.users_panel(lang=user['lang']))
        await state.set_state('in_start')

@dp.message_handler(state='in_settings')
async def in_settings_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(message.chat.id)
    if message.text[0] == '👤':
        await message.answer(text=_(f"😊 To'liq ismingizni kiriting.", locale=user[4]), reply_markup=await user_keyboards.cancel_btn(lang=user['lang']))
        await state.set_state('change_full_name')
    elif message.text[0] == '📞':
        await message.answer(text=_(f"😊 Telefon raqamingizni tugma orqali yuboring, yoki yozib yuboring."), reply_markup=await user_keyboards.phone_number(lang=user[4]))
        await state.set_state('change_phone_number')
    else:
        await message.answer(text=_(f"😊 O'zingizga qulay tilni tanlang.", locale=user['lang']), reply_markup=await user_keyboards.cancel_btn(lang=user[4]))
        await message.answer(text=_(f"Mavjud tillar", locale=user['lang']), reply_markup=languages)
        await state.set_state('change_lang')

@dp.callback_query_handler(state='change_lang')
async def change_lang_handler(call: types.CallbackQuery, state: FSMContext):
    await user_settings.change_lang(lang=call.data, chat_id=call.message.chat.id)
    await call.message.answer(text=_(f"😊 Muloqot tili o'zgartirildi.", locale=call.data), reply_markup=await user_keyboards.users_panel(call.data))
    await state.set_state('in_start')

@dp.message_handler(state='change_full_name')
async def change_full_name_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(message.from_user.id)
    await user_settings.change_full_name(full_name=message.text, chat_id=message.chat.id)
    await message.answer(text=_(f"😊 Ism muvaffaqqiyatli o'zgartirildi.", locale=user['lang']), reply_markup=await user_keyboards.users_panel(user['lang']))
    await state.set_state('in_start')

@dp.message_handler(state='change_phone_number', content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def change_phone_number_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(message.from_user.id)
    if await check_phone_number(phone_number=message.contact.phone_number if message.contact else message.text):
        await user_settings.change_phone_number(phone_number=f"+{message.contact.phone_number}" if message.contact else message.text, chat_id=message.chat.id)
        await message.answer(text=_(f"😊 Telefon raqam o'zgartirildi.", locale=user['lang']),reply_markup=await user_keyboards.users_panel(user['lang']))
        await state.set_state('in_start')
    else:
        userga = _(f"😕 Kechirasiz ")
        userga += user['full_name']
        userga += _(f" siz telefon raqamingizni no'tog'ri kiritdingiz. Tekshirib qayta kiriting yoki '📞 Telefon raqam yuborish' tugmasi orqali yuboring.\nNa'muna: +998999999999")
        await message.answer(text=userga, reply_markup=await user_keyboards.phone_number(lang=user['lang']))
        await state.set_state('change_phone_number')

@dp.message_handler(state='write_comment', content_types=types.ContentType.TEXT)
async def user_write_comment(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    adminga = f"""
📝 Foydalanuvchidan yangi xabar

👤 Toliq ism: {user['full_name']}
🔖 Username: {user['username']}
✍️ Xabar:
<b>{message.text}</b>
"""
    for admin in await admins.get_all_admins():
        await dp.bot.send_message(chat_id=admin['chat_id'], text=adminga)
    await message.answer(text=_(f"😊 Xabaringiz adminlarga yuborildi!", locale=user['lang']), reply_markup=await user_keyboards.users_panel(lang=user['lang']))
    await state.set_state('in_start')
