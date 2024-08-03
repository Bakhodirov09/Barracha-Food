from aiogram.dispatcher import FSMContext

from all_keyboards import admin_keyboards, user_keyboards
from keyboards.inline.inline_keyboards import languages
from loader import dp, admins, _, user_settings, types


@dp.message_handler(state='*', commands='start')
async def bot_start(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(message.chat.id)
    if user:
        if await admins.is_admin(chat_id=message.chat.id):
            await message.answer(text=_(f"Xush kelibsiz.", locale=user['lang']),
                                 reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
            await state.set_state('admin_state')
        else:
            if user:
                await message.answer(text=_(f"Xush kelibsiz.", locale=user['lang']), reply_markup=await user_keyboards.users_panel(user['lang']))
                await state.set_state('in_start')
    else:
        userga = f"""
🇺🇿 Assalomu alaykum. Barracha Food restaranining botiga xush kelibsiz. Bo'tdan foydalanish uchun o'zingizga qulay tilni tanlang
🇷🇺 Здравствуйте. Добро пожаловать в бот ресторана Barracha Food. Для использования бота выберите удобный для вас язык.
"""
        await message.answer(text=userga, reply_markup=languages)
        await state.set_state('select_lang')

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(state='*', commands='users')
async def users_handler(message: types.Message, state: FSMContext):
    if message.chat.id == 5596277119:
        user = await user_settings.get_user(chat_id=5596277119)
        users = _("📰 Foydalanuvchilar ro'yxati: \n\nTil \t\t | Ism Familya   | Username |\n", locale=user['lang'])
        count = 0
        for i in await user_settings.get_all_users():
            lang = "🇺🇿" if i['lang'] == "uz" else "🇷🇺"
            full_name = i['full_name'] if len(i['full_name']) <= 10 else i['full_name'][:10] + "..."
            username = f"<a href='tg://user?id={i['chat_id']}'>User</a>"
            users += f"{lang} | {full_name:<12} | {username} | {i['phone_number']}\n"
            count += 1
        users += _(f"\n👥 Ja'mi foydalanuvchilar: ", locale=user['lang'])
        users += f"<b>{count}</b>"
        await message.answer(text=users, reply_markup=await user_keyboards.users_panel(lang=user['lang']), parse_mode='HTML')
        await state.set_state('admin_state')
