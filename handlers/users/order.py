from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp, types, _, user_settings, other
from location import get_location_name
from all_keyboards import user_keyboards
from aiogram.dispatcher import FSMContext
from utils.send_order import send_order_to_channel


@dp.message_handler(state='select_order_type')
async def select_order_type_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    num = 0
    if message.text[0] == "🚚":
        num = 0
        data = await state.get_data()
        userga = _(f"\n🤗 Davom etish uchun yetkazib berish joylashuvini yuboring yoki '🗺 Mening manzillarim' tugmasi orqali manzil tanlang.", locale=user['lang'])
        await message.answer(text=userga, reply_markup=await user_keyboards.locations(lang=user['lang']))
        await state.set_state('select_or_send_location')
    elif message.text[0] == "🚶":
        num = 1
        filials_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        filials_btn.insert(KeyboardButton(text=_('⬅️ Ortga', locale=user['lang'])))
        filials_btn.insert(KeyboardButton(text=_('❌ Bekor qilish', locale=user['lang'])))
        for filial in await other.get_all_filials(lang=user['lang']):
            filials_btn.insert(KeyboardButton(text=f"📍 {filial['name']}"))
        await message.answer(text=_(f"🤗 Buyurtmangizni qaysi filialimizdan olib ketmoqchisiz?", locale=user['lang']), reply_markup=filials_btn)
        await state.set_state('select_filial_to_get_order')
    await state.update_data({
        'order_type': num
    })

@dp.message_handler(state='select_filial_to_get_order')
async def select_filial_to_get_order_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if await other.get_filial(name=message.text[2:]):
        await state.update_data({
            'filial': message.text[2:]
        })
        await message.answer(text=_(f'❓ Haqiqatdan ham ushbu filialimizga buyurtma bermoqchimisiz?', locale=user['lang']), reply_markup=await user_keyboards.accept(lang=user['lang']))
        await state.set_state('are_you_accept')
    else:
        filials_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        filials_btn.insert(KeyboardButton(text=_('⬅️ Ortga', locale=user['lang'])))
        filials_btn.insert(KeyboardButton(text=_('❌ Bekor qilish', locale=user['lang'])))
        for filial in await other.get_all_filials(lang=user['lang']):
            filials_btn.insert(KeyboardButton(text=f"📍 {filial['name']}"))
        await message.answer(text=_(f"😕 Kechirasiz bro siz noto'g'ri filial kiritdingiz iltimos qayta tekshirib kiriting.", locale=user['lang']), reply_markup=filials_btn)
        await state.set_state('select_filial_to_get_order')

@dp.message_handler(state='are_you_accept')
async def are_you_accept_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text.split(' ')[0] == "✅":
        data = await state.get_data()
        userga = _(f"✅ Buyurtmangiz qabul qilindi\n🆔 Buyurtma raqamingiz: ")
        number = await send_order_to_channel(chat_id=message.chat.id, date=message.date, data=data)
        userga += number
        await message.answer(text=userga, reply_markup=await user_keyboards.users_panel(lang=user['lang']))
        await state.set_state('in_start')
    else:
        await message.answer(text=_(f"😊 Buyurtmangiz bekor qilindi. Agar qayta buyurtma bermoqchi bo'lsangiz '🛍 Savat' tugmasini bosing"))

@dp.message_handler(state='select_or_send_location', content_types=types.ContentType.LOCATION)
async def select_or_send_location_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    address = await get_location_name(latitude=message.location.latitude, longitude=message.location.longitude, lang=user['lang'])
    location = f"{address[-1][1:]} {address[-3]} {address[-5]} {address[-4]} {address[0]}"
    await state.update_data({
        'address': location,
        'latitude': message.location.latitude,
        'longitude': message.location.longitude
    })
    userga = _(f"Siz yuborgan manzil:\n", locale=user['lang'])
    userga += f"<b>{location}</b>\n"
    userga += _(f"Ushbu manzilni tasdiqlaysizmi?", locale=user['lang'])
    await message.answer(text=userga, reply_markup=await user_keyboards.accept(lang=user['lang']))
    await state.set_state('accept_location')

@dp.message_handler(state='accept_location')
async def accept_location_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text[0] == "✅":
        data = await state.get_data()
        await state.update_data({
            'address': data['address'],
            'latitude': data['latitude'],
            'longitude': data['longitude']
        })
        await user_settings.add_to_locations(user_id=user['id'], location=data['address'], latitude=data['latitude'], longitude=data['longitude'])
        if "sergeli" in data['address'].lower():
            userga = _(f"✅ Buyurtmangiz qabul qilindi\n🆔 Buyurtma raqamingiz: ")
            number = await send_order_to_channel(chat_id=message.chat.id, date=message.date, data=data, plus_sum=0)
            userga += number
            await message.answer(text=userga, reply_markup=await user_keyboards.users_panel(lang=user['lang']))
            await state.set_state('in_start')
        else:
            userga = _(f"‼️ Eslatib o'tamiz hurmatli foydalanuvchi. Bizda dostavka xizmatimiz sergelidan boshqa hududlarga 15000 so'm bo'lganligi sabab sizning ja'mi to'laydigan summangiz: ")
            userga += f"<b>{data['total'] + 15000}</b> "
            userga += _(f"so'm bo'ladi‼️\n\nUshbu miqdordagi summani to'lashga rozimisiz?")
            await message.answer(text=userga, reply_markup=await user_keyboards.accept(lang=user['lang']))
            await state.set_state('accept_to_pay_sum')
    elif message.text[0] == "❌":
        await message.answer(text=_(f"‼️Iltimos qayta manzil yuboring.", locale=user['lang']), reply_markup=await user_keyboards.locations(lang=user['lang']))
        await state.set_state('select_or_send_location')

@dp.message_handler(state='accept_to_pay_sum')
async def accept_to_pay_sum_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text[0] == "✅":
        data = await state.get_data()
        await user_settings.add_to_locations(user_id=user['id'], location=data['address'], latitude=data['latitude'], longitude=data['longitude'])
        userga = _(f"✅ Buyurtmangiz qabul qilindi\n🆔 Buyurtma raqamingiz: ")
        number = await send_order_to_channel(chat_id=message.chat.id, date=message.date, data=data)
        userga += number
        await message.answer(text=userga, reply_markup=await user_keyboards.users_panel(lang=user['lang']))
    else:
        await message.answer(text=_(f"✅ Buyurtmangiz bekor qilindi.", locale=user['lang']), reply_markup=await user_keyboards.users_panel(lang=user['lang']))
    await state.set_state('in_start')


@dp.message_handler(state='select_or_send_location')
async def select_location_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    user_locations = await user_settings.get_user_locations(user_id=user['id'])
    if user_locations:
        locations_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        locations_btn.insert(KeyboardButton(text=_(f"⬅️ Ortga", locale=user['lang'])))
        locations_btn.insert(KeyboardButton(text=_(f"❌ Bekor qilish", locale=user['lang'])))
        locations_btn.row_width = 1
        for location in user_locations:
            locations_btn.insert(KeyboardButton(text=location['name']))
        await message.answer(text=_(f"🤗 Yetkazib berish joylashuvini tanlang", locale=user['lang']), reply_markup=locations_btn)
        await state.set_state('select_location')
    else:
        await message.answer(text=_(f"😕 Kechirasiz bizning botimizda sizning manzilaringiz mavjud emas!", locale=user['lang']))
        await state.set_state('select_or_send_location')

@dp.message_handler(state='select_location')
async def select_location_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    user_location = await user_settings.get_user_location(user_id=user['id'], name=message.text)
    if user_location:
        await state.update_data({
            'address': message.text,
            'latitude': user_location['latitude'],
            'longitude': user_location['longitude'],
        })
        data = await state.get_data()
        if "sergeli" in message.text.lower():
            number = await send_order_to_channel(chat_id=message.chat.id, date=message.date, data=data, plus_sum=0)
            userga = _(f"✅ Buyurtmangiz qabul qilindi\n🆔 Buyurtma raqamingiz: ")
            userga += number
            await message.answer(text=userga, reply_markup=await user_keyboards.users_panel(lang=user['lang']))
            await state.set_state('in_start')
        else:
            userga = _(f"‼️ Eslatib o'tamiz hurmatli foydalanuvchi. Bizda dostavka xizmatimiz sergelidan boshqa hududlarga 15000 so'm bo'lganligi sabab sizning ja'mi to'laydigan summangiz: ")
            userga += f"<b>{data['total'] + 15000}</b> "
            userga += _(f"so'm bo'ladi‼️\n\nUshbu miqdordagi summani to'lashga rozimisiz?")
            await message.answer(text=userga, reply_markup=await user_keyboards.accept(lang=user['lang']))
            await state.set_state('accept_to_pay_sum')
    else:
        await message.answer(text=_(f"😕 Kechirasiz siz noto'g'ri manzil tanladingiz.", locale=user['lang']), reply_markup=await user_keyboards.locations(lang=user['lang']))
        await state.set_state('select_or_send_location')