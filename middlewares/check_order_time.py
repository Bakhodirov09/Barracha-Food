from datetime import time
from loader import types, _


class CheckOrderTime:
    async def check_order_time(self, message: types.Message, user):
        date = message.date
        local_time = date.time()

        start_time = time(9, 0)
        end_time = time(3, 0)

        if start_time <= local_time or local_time <= end_time:
            return True
        else:
            await message.answer(_(f"😕 Kechirasiz bizning ish vaqtimiz 09:00 dan 03:00 gacha. Siz faqat ushbu vaqt oralig'gida bbizga buyurtma berishingiz mumkin.", locale=user['lang']))
            return False
