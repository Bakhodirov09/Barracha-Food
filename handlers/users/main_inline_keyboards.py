from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.inline_keyboards import plus_minus
from loader import _, admins, user_settings, dp, types, basket_settings, menu


@dp.callback_query_handler(state='*')
async def inline_keyboards_handler(call: types.CallbackQuery, state: FSMContext):
    user = await user_settings.get_user(chat_id=call.message.chat.id)
    data = call.data.split('_')
    if data[0] == "plus":
        baza = await basket_settings.plus(product_id=int(data[1]), user_id=int(user['id']))
        try:
            await call.message.edit_reply_markup(reply_markup=await plus_minus(back_menu=data[-1], food_id=data[1], price=int(baza[0]['quantity']) * int(baza[1]['price']), quantity=baza[0]['quantity'], lang=user['lang']))
        except:
            await call.answer(text=_(f"✅ Muvaffaqqiyatli",locale=user['lang']))
    elif data[0] == "minus":
        baza = await basket_settings.minus(product_id=int(data[1]), user_id=int(user['id']))
        if type(baza) == tuple:
            try:
                await call.message.edit_reply_markup(reply_markup=await plus_minus(back_menu=data[-1], food_id=data[1], price=int(baza[0]['quantity']) * int(baza[1]['price']), quantity=baza[0]['quantity'], lang=user['lang']))
            except:
                await call.answer(text=_(f"✅ Muvaffaqqiyatli",locale=user['lang']))
        elif baza == False:
            await call.answer(text=_("😕 Kechirasiz mahsulotni kamaytirish uchun, mahsulot savatingizda kamida 1 dona bo'lishi kerak.", locale=user['lang']), show_alert=True)
        elif baza == 'DELETED':
            await call.answer(text=_("✅ Mahsulot savatingizdan olib tashlandi.", locale=user['lang']), show_alert=True)
            await call.message.edit_reply_markup(reply_markup=await plus_minus(back_menu=data[-1], food_id=data[1], price=0, quantity=0, lang=user['lang']))
    else:
        await call.message.delete()
        menu_btn = InlineKeyboardMarkup(row_width=2)
        menu_btn.insert(InlineKeyboardButton(text=_('⬅️ Ortga', locale=user['lang']), callback_data='back_to_menu'))
        menu_btn.insert(InlineKeyboardButton(text=_('🛍 Savat', locale=user['lang']), callback_data='basket'))
        menu_name = await menu.get_menu_photo(menu_id=int(call.data.split('_')[-1]))
        userga = f"{menu_name['name']} "
        userga += _(f"menyusi", locale=user['lang'])
        for food in await menu.get_menu_foods(menu_id=int(call.data.split('_')[-1]), lang=user['lang']):
            menu_btn.insert(InlineKeyboardButton(text=food['name'], callback_data=f"{menu_name['name']}_{food['menu_id']}_{food['name']}"))
        await call.message.answer_photo(photo=menu_name['photo'], caption=userga, reply_markup=menu_btn)
        await state.set_state('in_foods')