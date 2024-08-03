from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from middlewares.language import setup_middleware
from utils.db_api.database_functions import AdminSettings, MenuFunction, UserSettings, OtherSettings, BasketSettings

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Database classes
admins = AdminSettings()
menu = MenuFunction()
user_settings = UserSettings()
other = OtherSettings()
basket_settings = BasketSettings()

# i18n Settings
i18n = setup_middleware(dp)

_ = i18n.gettext