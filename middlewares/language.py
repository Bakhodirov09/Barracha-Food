from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from typing import Any, Tuple, Optional

from aiogram.types import ReplyKeyboardRemove

import loader
from main.config import I18N_DOMAIN, LOCALES_DIR
from aiogram.contrib.middlewares.i18n import I18nMiddleware


async def get_lang(user_id):
    user = await loader.user_settings.get_user(user_id)
    if user and user['status'] is False:
        return ("USER_BLOCKED", user['days'], user['time'], user['lang'])
    elif user:
        return user['lang']
    else:
        return 'uz'


class ACLMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, data: dict):
        date = 0
        if update.message:
            date = update.message.date
            user_id = update.message.from_user.id
        elif update.callback_query:
            date = update.callback_query.message.date
            user_id = update.callback_query.from_user.id
        else:
            return

        user_lang = await get_lang(user_id)
        if user_lang[0] == "USER_BLOCKED":
            if user_lang[2] > date:
                text = loader._("‼️ Kechirasiz bro. Siz ushbu botda admin tomonidan ", locale=user_lang[-1])
                text += f"{user_lang[1]} "
                text += loader._(f"kunga blok bo'lgansiz.")
                if update.message:
                    await update.message.reply(text=text, reply_markup=ReplyKeyboardRemove())
                elif update.callback_query:
                    await update.callback_query.message.reply(text=text, reply_markup=ReplyKeyboardRemove())
                raise CancelHandler()
            else:
                userga = loader._(f"🥳 Tabriklaymiz hurmatli foydalanuvchi sizning ", locale=user_lang[-1])
                userga += f"{user_lang[1]} "
                userga += loader._(f"kunlik blok holatingiz o'z nihoyasiga yetdi. Botimizdan faol foydalanishingiz mumkin. Botimizdan foydalanish uchun avvalo /start buyrug'ini kiriting.", locale=user_lang[-1])
                chat_id = 0
                if update.message:
                    chat_id = update.message.chat.id
                    await update.message.answer(text=userga, reply_markup=ReplyKeyboardRemove())
                elif update.callback_query:
                    chat_id = update.callback_query.message.chat.id
                    await update.callback_query.message.answer(text=userga, reply_markup=ReplyKeyboardRemove())
                await loader.admins.unblock_user(chat_id=chat_id)

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user_ = types.User.get_current()
        return await get_lang(user_.id)

class IsProgrammer(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        access_chat_ids = [5596277119, 796142416, 6354162965, 1687544010, 572592302]
        if update.message:
            if update.message.chat.id in access_chat_ids:
                return
            else:
                print(update.message.chat.id)
                await update.message.answer(text=f"‼️ Kechirasiz bro. Bot hozirda dasturchi tomonidan tuzib chiqilmoqda. Bot rasman 3 yoki 5 Avgust kuni to'liq ishga tushiriladi. Iltimos sabrli bo'ling! 😊")
                raise CancelHandler()
        elif update.callback_query:
            if update.callback_query.message.chat.id in access_chat_ids:
                return
            else:
                print(update.callback_query.message.chat.id)
                await update.callback_query.message.answer(text=f"‼️ Kechirasiz bro. Bot hozirda dasturchi tomonidan tuzib chiqilmoqda. Bot rasman 3 yoki 5 Avgust kuni to'liq ishga tushiriladi. Iltimos sabrli bo'ling! 😊")
                raise CancelHandler()

def setup_middleware(dp):
    i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
    acl = ACLMiddleware()
    is_dev = IsProgrammer()
    dp.middleware.setup(is_dev)
    dp.middleware.setup(i18n)
    dp.middleware.setup(acl)
    return i18n