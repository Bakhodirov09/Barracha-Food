from main.database_settings import database
from main.models import admins


async def is_admin(self, chat_id):
    return await database.fetchone(query=admins.select().where(admins.c.chat_id == chat_id))

