from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _, admins, user_settings, dp, types, basket_settings, menu
from all_keyboards import user_keyboards, admin_keyboards

@dp.message_handler(state='*', text=['❌ Bekor qilish', '❌ Отмена', '🏘 Asosiy menyu', '🏘 Главное меню'])
async def cancel_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    userga = _(f"✅ Bekor qilindi", locale=user['lang']) if message.text[0] == "❌" else _(f"🏘 Asosiy menyu", locale=user['lang'])
    if await admins.is_admin(chat_id=message.chat.id):
        await message.answer(text=userga, reply_markup=await admin_keyboards.admins_panel(lang=user['lang']))
        await state.set_state('admin_state')
    else:
        await message.answer(text=userga, reply_markup=await user_keyboards.users_panel(lang=user['lang']))
        await state.set_state('in_start')

@dp.message_handler(state='*', text=['🛍 Savat', '🛍 Savat'])
async def basket_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    basket = await basket_settings.get_user_basket(user_id=user['id'])
    if basket:
        userga = _(f"🛍 Sizning savatingiz\n\n", locale=user['lang'])
        counter = 1
        basket_btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        basket_btn.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user['lang'])))
        basket_btn.insert(KeyboardButton(text=_(f"🛒 Buyurtma berish", locale=user['lang'])))
        basket_btn.row_width = 1
        total = 0
        for product in basket:
            mah = await menu.get_food_with_id(product['product_id'])
            basket_btn.insert(KeyboardButton(text=f"❌ {mah['name']}"))
            userga += f"<b>{counter}</b>. <b>{mah['name']}</b> | {mah['price']} * {product['quantity']} = {mah['price'] * product['quantity']}\n"
            counter += 1
            total += product['quantity'] * mah['price']
        userga += _(f"\n💰 Ja'mi: ")
        userga += f"<b>{total}</b>"
        await message.answer(text=userga, reply_markup=basket_btn)
        await state.set_state('in_basket')
    else:
        await message.answer(text=_(f"😕 Kechirasiz sizning savatingiz bo'sh", locale=user['lang']))

@dp.callback_query_handler(state='*', text='basket')
async def basket_handler(call: types.CallbackQuery, state: FSMContext):
    user = await user_settings.get_user(chat_id=call.message.chat.id)
    basket = await basket_settings.get_user_basket(user_id=user['id'])
    if basket:
        userga = _(f"🛍 Sizning savatingiz\n\n", locale=user['lang'])
        counter = 1
        basket_btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        basket_btn.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu",locale=user['lang'])))
        basket_btn.insert(KeyboardButton(text=_(f"🛒 Buyurtma berish",locale=user['lang'])))
        basket_btn.row_width = 1
        total = 0
        for product in basket:
            mah = await menu.get_food_with_id(product['product_id'])
            basket_btn.insert(KeyboardButton(text=f"❌ {mah['name']}"))
            userga += f"<b>{counter}</b>. <b>{mah['name']}</b> | {mah['price']} * {product['quantity']} = {mah['price'] * product['quantity']}\n"
            counter += 1
            total += product['quantity'] * mah['price']
        userga += _(f"\n💰 Ja'mi: ")
        userga += f"<b>{total}</b>"
        await call.message.answer(text=userga, reply_markup=basket_btn)
        await state.set_state('in_basket')
    else:
        await call.message.answer(text=_(f"😕 Kechirasiz sizning savatingiz bo'sh", locale=user['lang']))

@dp.message_handler(state='in_basket')
async def in_basket_handler(message: types.Message, state: FSMContext):
    user = await user_settings.get_user(chat_id=message.chat.id)
    if message.text[0] == "❌":
        product = message.text[2:]
        product_id = await menu.get_food_with_name(product_name=product)
        await basket_settings.remove_product(product_id=int(product_id['id']), user_id=int(user['id']))
        basket = await basket_settings.get_user_basket(user_id=user['id'])
        await message.answer(text=_(f"✅ Mahsulot savatingizdan olib tashlandi.", locale=user['lang']), reply_markup=await user_keyboards.users_panel(lang=user['lang']))
        await state.set_state('in_start')
        if basket:
            userga = _(f"🛍 Sizning savatingiz\n\n", locale=user['lang'])
            counter = 1
            total = 0
            basket_btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            basket_btn.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user['lang'])))
            basket_btn.insert(KeyboardButton(text=_(f"🛒 Buyurtma berish", locale=user['lang'])))
            basket_btn.row_width = 1
            for i in basket:
                mah = await menu.get_food_with_id(i['product_id'])
                basket_btn.insert(KeyboardButton(text=f"❌ {mah['name']}"))
                userga += f"<b>{counter}</b>. <b>{mah['name']}</b> | {mah['price']} * {i['quantity']} = {mah['price'] * i['quantity']}\n"
                total += i['quantity'] * mah['price']
            userga += _(f"\n💰 Ja'mi: ", locale=user['lang'])
            userga += str(total)
            await message.answer(text=userga, reply_markup=basket_btn)
            await state.set_state('in_basket')
    else:
        await message.answer(text=_(f"🤗 Buyurtma turini tanlang.", locale=user['lang']), reply_markup=await user_keyboards.order_type(lang=user['lang']))
        await state.set_state('select_order_type')