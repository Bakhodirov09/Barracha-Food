from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.inline_keyboards import languages
from loader import dp, _, user_settings
from all_keyboards import user_keyboards, admin_keyboards


# Echo bot
@dp.message_handler(state='*')
async def bot_echo(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if user:
        await message.answer(text=_(f"🏘 Asosiy menyu", locale=user['lang']), reply_markup=await user_keyboards.users_panel(lang=user['lang']))
        await state.set_state('in_start')
    else:
        userga = f"""
🇺🇿 Assalomu alaykum. Barracha Food restaranining botiga xush kelibsiz. Bo'tdan foydalanish uchun o'zingizga qulay tilni tanlang
🇷🇺 Здравствуйте. Добро пожаловать в бот ресторана Barracha Food. Для использования бота выберите удобный для вас язык.
"""
        await message.answer(text=userga, reply_markup=languages)
        await state.set_state('select_lang')
