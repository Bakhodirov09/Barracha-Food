from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from loader import dp, _, user_settings
from aiogram.dispatcher import FSMContext
from all_keyboards import admin_keyboards, user_keyboards
from regex import check_phone_number


@dp.callback_query_handler(state='select_lang')
async def select_lang_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({
        'lang': call.data
    })
    await call.message.delete()
    await call.message.answer(text=_(f"🇺🇿 Uzbek tili tanlandi. Iltimos toliq ismingizni yozing.", locale=call.data))
    await state.set_state('write_full_name')

@dp.message_handler(state='write_full_name')
async def write_full_name_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({
        'lang': data['lang'],
        "full_name": message.text
    })
    await message.answer(text=_(f"📞 Iltimos telefon raqamingizni yuboring"), reply_markup=await user_keyboards.phone_number(lang=data['lang']))
    await state.set_state('send_phone_number')

@dp.message_handler(state='send_phone_number', content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def send_phone_number_handler(message: types.Message, state: FSMContext):
    check_phone = await check_phone_number(phone_number=message.contact.phone_number if message.contact else message.text)
    if check_phone:
        state_data = await state.get_data()
        await state.update_data({
            'phone_number': f"{message.contact.phone_number}" if message.contact else message.text,
            'username': f"@{message.from_user.username}" if message.from_user.username != None else 'Username mavjud emas',
            'full_name': state_data['full_name'],
            'chat_id': message.chat.id
        })
        data = await state.get_data()
        await user_settings.insert_user(data=data)
        await message.answer(text=_(f"🥳 Tabriklaymiz. Siz botimizdan muvaffaqqiyatli ro'yxatdan o'tdingiz.", locale=data['lang']), reply_markup=await user_keyboards.users_panel(lang=data['lang']))
        await state.set_state('in_start')
    else:
        data = await state.get_data()
        await state.update_data({
            'full_name': data['full_name'],
            'lang': data['lang']
        })
        userga = _(f"😕 Kechirasiz ")
        userga += data['full_name']
        userga += _(
            f" siz telefon raqamingizni no'tog'ri kiritdingiz. Tekshirib qayta kiriting yoki '📞 Telefon raqam yuborish' tugmasi orqali yuboring.\nNa'muna: +998999999999")
        await message.answer(text=userga, reply_markup=await user_keyboards.phone_number(lang=data['lang']))
        await state.set_state('send_phone_number')
