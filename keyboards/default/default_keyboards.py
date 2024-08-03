from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import loader

class UserKeyboards:
    async def phone_number(self, lang):
        send_phone_number = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"📞 Telefon raqam yuborish", locale=lang), request_contact=True)
                ]
            ], resize_keyboard=True
        )
        return send_phone_number

    async def filials_and_socials(self, lang):
        filials_socials_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"📍 Filiallar", locale=lang)),
                    KeyboardButton(text=loader._(f"🌐 Ijtimoiy tarmoqlar", locale=lang)),
                ],
                [
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return filials_socials_btn

    async def user_settings_menu(self, lang):
        settings = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"👤 Ism Familyani O'zgartirish", locale=lang)),
                    KeyboardButton(text=loader._(f"📞 Telefon Raqamni O'zgartirish", locale=lang)),
                ],
                [
                    KeyboardButton(text=loader._(f"🇺🇿 🔁 🇷🇺 Tilni O'zgartirish", locale=lang)),
                    KeyboardButton(text=loader._(f"🏘 Asosiy Menyu", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return settings

    async def users_panel(self, lang):
        users_menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"🍴 Menyu", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"🛍 Mening buyurtmalarim", locale=lang)),
                    KeyboardButton(text=loader._(f"✍️ Izoh qoldirish", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"ℹ️ Biz haqimizda", locale=lang)),
                    KeyboardButton(text=loader._(f"📍🌐 Filiallar va Ijtimoiy tarmoqlar", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"⚙️ Sozlamalar", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return users_menu

    async def main_menu_basket(self, lang):
        main_menu_basket_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"🏘 Asosiy menyu", locale=lang)),
                    KeyboardButton(text=loader._(f"🛍 Savat", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return main_menu_basket_btn

    async def accept(self, lang):
        accept_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"✅ Xa", locale=lang)),
                    KeyboardButton(text=loader._(f"❌ Yo'q", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return accept_btn

    async def cancel_btn(self, lang):
        cancel_button = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return cancel_button

    async def locations(self, lang):
        locations_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"🗺 Mening manzillarim", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"📍 Joylashuv yuborish", locale=lang), request_location=True),
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return locations_btn

    async def send_location(self, lang):
        send_loc = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._("📍 Joylashuv yuborish", locale=lang), request_location=True)
                ]
            ], resize_keyboard=True
        )
        return send_loc

    async def order_type(self, lang):
        order_type_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"🚶 Borib olish", locale=lang)),
                    KeyboardButton(text=loader._(f"🚚 Dostavka", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return order_type_btn

class AdminKeyboards:
    async def admins_panel(self, lang):
        admin_panel = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"🍴 Menyu sozlamalari", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"🍽 Menyu", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"✍️ Xabar yuborish")),
                    KeyboardButton(text=loader._(f"🏷 Aksiya", locale=lang)),
                ],
                [
                    KeyboardButton(text=loader._(f"📍 Filiallar", locale=lang)),
                    KeyboardButton(text=loader._(f"👥 Foydalanuvchilar", locale=lang)),
                ],
                [
                    KeyboardButton(text=loader._(f"👤 Adminlar", locale=lang)),
                    KeyboardButton(text=loader._(f"🌐 Ijtimoiy tarmoqlar", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"🔁 Logo o'zgartirish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return admin_panel

    async def menu_settings(self, lang):
        menu_settings_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"➕🍴 Menyu qoshish", locale=lang)),
                    KeyboardButton(text=loader._(f"🚫🍴 Menyu ochirish", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"➕🌯 Taom qoshish", locale=lang)),
                    KeyboardButton(text=loader._(f"🚫🌯 Taom ochirsh", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"🔧💰 Taom narxini o'zgartirish", locale=lang)),
                    KeyboardButton(text=loader._(f"🔧🖼 Taom rasmini o'zgartirish", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return menu_settings_btn

    async def admin_user_settings(self, lang):
        admin_user_settings_btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=loader._(f"❌ Foydalanuvchi ochirish", locale=lang), callback_data='delete_user')
                ],
                [
                    InlineKeyboardButton(text=loader._(f"🚫 Foydalanuvchi bloklash", locale=lang), callback_data='block_user')
                ],
            ]
        )
        return admin_user_settings_btn

    async def stock_settings(self, lang):
        stock_settings_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"🏷 Aksiya yoqish ochirish", locale=lang)),
                    KeyboardButton(text=loader._(f"➕🏷 Aksiyaga taom qoshish", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return stock_settings_btn

    async def filial_settings(self, lang):
        filial_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"➕📍 Filial qoshish", locale=lang)),
                    KeyboardButton(text=loader._(f"🚫📍 Filial olib tashlash", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"❌ Bekor qilish"))
                ]
            ], resize_keyboard=True
        )
        return filial_btn

    async def admins(self, lang):
        admins_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"➕👤 Admin qoshish", locale=lang)),
                    KeyboardButton(text=loader._(f"🚫👤 Admin olib tashlash", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"👤 Adminlar", locale=lang)),
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return admins_btn

    async def socials(self, lang):
        socials_btn = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loader._(f"➕🌐 Ijtimoiy tarmoq qoshish", locale=lang)),
                    KeyboardButton(text=loader._(f"🚫🌐 Ijtimoiy tarmoq ochirish", locale=lang))
                ],
                [
                    KeyboardButton(text=loader._(f"🌐 Ijtimoiy tarmoqlar", locale=lang)),
                    KeyboardButton(text=loader._(f"❌ Bekor qilish", locale=lang))
                ]
            ], resize_keyboard=True
        )
        return socials_btn