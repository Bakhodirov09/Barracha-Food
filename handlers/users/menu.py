from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from all_keyboards import user_keyboards
from keyboards.inline.inline_keyboards import plus_minus
from loader import dp, menu, types, _, user_settings, other


@dp.callback_query_handler(state='in_menu')
async def get_menu_foods_handler(call: types.CallbackQuery, state: FSMContext):
    user = await user_settings.get_user(chat_id=call.message.chat.id)
    if call.data.split('_')[0] != "back":
        foods_btn = InlineKeyboardMarkup(row_width=2)
        foods = await menu.get_menu_foods(menu_id=int(call.data.split('_')[-1]), lang=user['lang'])
        userga = f"{call.data.split('_')[0]} "
        userga += _(f"menyusi", locale=user['lang'])
        foods_btn.insert(InlineKeyboardButton(text=_(f"⬅️ Ortga", locale=user['lang']), callback_data=f"back_to_menu"))
        foods_btn.insert(InlineKeyboardButton(text=_(f"🛍 Savat", locale=user['lang']), callback_data=f"basket"))
        for food in foods:
            foods_btn.insert(InlineKeyboardButton(text=food['name'], callback_data=f"{call.data.split('_')[0]}_{food['menu_id']}_{food['name']}"))
        photo = await menu.get_menu_photo(menu_id=int(call.data.split('_')[-1]))
        await call.message.delete()
        await call.message.answer_photo(photo=photo['photo'], caption=userga, reply_markup=foods_btn)
        await state.set_state('in_foods')
    else:
        await call.message.delete()
        await call.message.answer(text=_(f"🏘 Asosiy menyu", locale=user['lang']), reply_markup=await user_keyboards.users_panel(lang=user['lang']))
        await state.set_state('in_start')
@dp.callback_query_handler(state='in_foods')
async def in_foods_handler(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    user = await user_settings.get_user(chat_id=call.message.chat.id)
    if data[0] == 'back':
        await call.message.delete()
        logo = await other.get_logo()
        menu_btn = InlineKeyboardMarkup(row_width=2)
        menu_btn.insert(InlineKeyboardButton(text=_(f"⬅️ Ortga", locale=user['lang']), callback_data='back_to_main_menu'))
        menu_btn.insert(InlineKeyboardButton(text=_(f"🛍 Savat", locale=user['lang']), callback_data='basket'))
        stock_status = await other.get_stock_status()
        if stock_status:
            menu_btn.insert(InlineKeyboardButton(text=_(f"Aksiya", locale=user['lang']), callback_data='stock'))
        for menyu in await menu.get_menu(lang=user['lang']):
            menu_btn.insert(InlineKeyboardButton(text=menyu['name'], callback_data=f"{menyu['name']}_{menyu['id']}"))
        await call.message.answer(text=_(f"😋 Bizning menyu", locale=user['lang']), reply_markup=await user_keyboards.main_menu_basket(lang=user['lang']))
        await call.message.answer_photo(photo=logo['photo'], reply_markup=menu_btn)
        await state.set_state('in_menu')
    else:
        try:
            food = await menu.get_food(menu_id=int(call.data.split('_')[1]), name=call.data.split('_')[-1])
            meal, desc, price = _('Taom', locale=user['lang']), _('Taom haqida', locale=user['lang']), _(f"Narxi", locale=user['lang'])
            userga = f"""
{meal}: {food['name']}

‼️ {desc} ‼️

- <b>{food['desc']}</b>

💰 {price}: {food['price']}
"""
            await call.message.delete()
            await call.message.answer_photo(photo=food['photo'], caption=userga, reply_markup=await plus_minus(
                back_menu=call.data.split('_')[1], food_id=food['id'], price=0, quantity=0, lang=user['lang']))
            await state.set_state('in_food')
        except Exception as e:
            pass