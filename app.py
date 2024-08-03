from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from main.database_settings import database
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await database.connect()

async def on_shutdown(dispatcher):
    await on_shutdown_notify(dispatcher)
    await database.disconnect()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
