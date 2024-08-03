from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 Uzbek tili", callback_data='uz')
        ],
        [
            InlineKeyboardButton(text=f"🇷🇺 Русский язык ", callback_data='ru')
        ]
    ]
)

async def plus_minus(back_menu, food_id, price, quantity, lang):
    plus_minus_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"➖", callback_data=f"minus_{food_id}_{back_menu}"),
                InlineKeyboardButton(text=f"{quantity} | {price}", callback_data=f"lala"),
                InlineKeyboardButton(text=f"➕", callback_data=f"plus_{food_id}_{back_menu}"),
            ],
            [
                InlineKeyboardButton(text=_(f"⬅️ Ortga", locale=lang), callback_data=f'back_to_menu_{back_menu}'),
            ],
            [
                InlineKeyboardButton(text=_(f"🛍 Savat", locale=lang), callback_data='basket')
            ]
        ]
    )
    return plus_minus_btn