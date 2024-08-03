from loader import user_settings, dp, basket_settings, menu
import random
from data.config import env

async def send_order_to_channel(chat_id, date, data: dict):
    user = await user_settings.get_user(chat_id=chat_id)
    number = ""
    for i in range(6):
        number += str(random.choice(range(10)))
    flag = ""
    if user['lang'] == "uz":
        flag = "🇺🇿"
    else:
        flag = "🇷🇺"
    adminga = f""
    if data['order_type'] == 1:
        adminga += f"🆕🛍 <b>{data['filial']}</b> uchun yangi buyurtma"
    else:
        adminga += f"🆕🛍 Yangi buyurtma: \n"
    adminga += f"""
👤 Ism: {user['full_name']}
👤 Username: {user['username']}
📞 Telefon raqam: {user['phone_number']}
🏳️ Tanlangan til: {flag}
🆔 Buyurtma raqam: {number}
🛒 Mahsulotlar:

"""
    total = 0
    for product in await basket_settings.get_user_basket(user_id=user['id']):
        mah = await menu.get_food_with_id(product['product_id'])
        adminga += f"{mah['name']} | {product['quantity']}\n"
        total += mah['price'] * product['quantity']
    order_type = ""
    if data['order_type'] == 0:
        order_type = "🚚 Dostavka"
    else:
        order_type = f"🚶 Olib ketish uchun"
    adminga += f"\n↩️ Buyurtma turi: <b>{order_type}</b>"
    if data['order_type'] == 0:
        adminga += f"\n📍Joylashuv: {data['address']}\n"
    adminga += f"\n💰 Ja'mi: {total}"
    if data.get('address', None):
        print(11)
        await user_settings.add_history_buys(user_id=user['id'], number=int(number), total=int(int(total)), address=data['address'], date=date, order_type=order_type)
        await dp.bot.send_location(chat_id=env.int('CHANNEL_ID'), latitude=data['latitude'],longitude=data['longitude'])
    else:
        print(22)
        await user_settings.add_history_buys(user_id=user['id'], number=int(number), total=int(int(total)), filial=data['filial'], date=date, order_type=order_type)
    await dp.bot.send_message(chat_id=env.int('CHANNEL_ID'), text=adminga)
    return number