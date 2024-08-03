from main.database_settings import database
from main.models import *
import loader

class UserSettings:
    async def get_user(self, chat_id):
        return await database.fetch_one(query=users.select().where(
            users.c.chat_id == chat_id
        ))

    async def insert_user(self, data):
        return await database.execute(query=users.insert().values(
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            username=data['username'],
            chat_id=data['chat_id'],
            lang=data['lang']
        ))

    async def get_all_users(self):
        return await database.fetch_all(query=users.select().order_by(users.c.id))

    async def get_user_locations(self, user_id):
        return await database.fetch_all(query=locations.select().where(
            locations.c.user_id == user_id
        ))

    async def get_user_location(self, user_id, name):
        return await database.fetch_one(query=locations.select().where(
            locations.c.user_id == user_id,
            locations.c.name.ilike(f"%{name}%")
        ))

    async def add_history_buys(self, user_id, number, total, date, order_type, address=None, filial=None):
        number_id = await database.execute(query=order_abouts.insert().values(
            number_id=number,
            number_uuid=uuid.uuid4(),
            total=total,
            user_id=user_id,
            date=date,
            where_to=address,
            which_filial=filial,
            type=order_type
        ).returning(order_abouts.c.id))
        for product in await loader.basket_settings.get_user_basket(user_id):
            await database.execute(query=history_buys.insert().values(
                number_id=number_id,
                food_id=product['product_id'],
                quantity=product['quantity'],
            ))

    async def add_to_locations(self, user_id, location, latitude=None, longitude=None):
        address = await self.get_user_location(user_id, location)
        if not address:
            return await database.execute(query=locations.insert().values(
                user_id=user_id,
                name=location,
                latitude=f"{latitude}",
                longitude=f"{longitude}"
            ))

    async def get_order_numbers(self, user_id):
        return await database.fetch_all(query=order_abouts.select().where(order_abouts.c.user_id == user_id))

    async def get_history_buys(self, number_id):
        return await database.fetch_all(query=history_buys.select().where(
            history_buys.c.number_id == number_id
        ))

    async def change_full_name(self, chat_id, full_name):
        return await database.execute(query=users.update().values(
            full_name=full_name,
        ).where(users.c.chat_id == chat_id))

    async def change_phone_number(self, chat_id, phone_number):
        return await database.execute(query=users.update().values(
            phone_number=phone_number
        ).where(users.c.chat_id == chat_id))

    async def change_lang(self, lang, chat_id):
        return await database.execute(query=users.update().values(
            lang=lang
        ).where(users.c.chat_id == chat_id))

class AdminSettings:
    async def is_admin(self, chat_id):
        return await database.fetch_one(query=admins.select().where(admins.c.chat_id == chat_id))

    async def get_admin(self, id=None):
        return await database.fetch_one(query=admins.select().where(admins.c.id == id))

    async def delete_admin(self, id):
        return await database.execute(query=admins.delete().where(
            admins.c.id == id
        ))

    async def add_admin(self, chat_id):
        return await database.execute(query=admins.insert().values(
            chat_id=chat_id
        ))

    async def get_all_admins(self):
        return await database.fetch_all(query=admins.select().order_by(admins.c.id))

    async def delete_user(self, pk):
        return await database.execute(query=users.delete().where(users.c.id == pk))

    async def block_user(self, pk):
        return await database.execute(query=users.update().values(status=False).where(
            users.c.id == pk
        ))


class MenuFunction:
    async def add_menu(self, data):
        await database.execute(query=menu.insert().values(
            photo=data['photo'],
            lang='uz',
            name=data['uz'],
            name_to_get=data['uz']
        ))

        await database.execute(query=menu.insert().values(
            photo=data['photo'],
            lang='ru',
            name=data['ru'],
            name_to_get=data['uz']
        ))
        return True

    async def get_food_with_name(self, product_name):
        return await database.fetch_one(query=foods.select().where(
            foods.c.name == product_name
        ))

    async def add_food(self, data):
        menyu = await self.get_menu_with_name(menu_name=data['menu'], lang=data['lang'])
        menyu_uz = await self.get_menu_with_name(menu_name=menyu['name_to_get'])
        menyu_ru = await self.get_menu_with_name(menu_name=menyu['name_to_get'])
        await database.execute(query=foods.insert().values(
            photo=data['photo'],
            name=data['name_uz'],
            price=data['price'],
            desc=data['desc_uz'],
            menu_id=menyu_uz['id'],
            lang='uz'
        ))
        await database.execute(query=foods.insert().values(
            photo=data['photo'],
            name=data['name_ru'],
            price=data['price'],
            desc=data['desc_ru'],
            menu_id=menyu_ru['id'],
            lang='ru'
        ))
        return True

    async def get_menu_photo(self, menu_id):
        return await database.fetch_one(query=menu.select().where(
            menu.c.id == menu_id
        ))

    async def change_food_price(self, data):
        food = await self.get_food(menu_id=data['menu_id'], name=data['name'])
        return await database.execute(query=foods.update().values(
            price=data['new_price']
        ).where(foods.c.photo == food['photo']))

    async def get_menu(self, lang):
        return await database.fetch_all(query=menu.select().where(
            menu.c.lang == lang
        ).order_by(menu.c.id))

    async def get_menu_with_name(self, menu_name, lang='uz'):
        return await database.fetch_one(query=menu.select().where(
            menu.c.name == menu_name,
            menu.c.lang == lang
        ))

    async def delete_menu(self, menu_name):
        menuu = await self.get_menu_with_name(menu_name)
        await database.execute(query=menu.delete().where(
            name=menu_name
        ))
        await database.execute(query=menu.delete().where(
            name_to_get=menuu['name_to_get']
        ))
        return True

    async def get_menu_foods(self, menu_id, lang):
        return await database.fetch_all(query=foods.select().where(
            foods.c.menu_id == menu_id,
            foods.c.lang == lang
        ))

    async def delete_food(self, data):
        food = await self.get_food(menu_id=data['menu_id'], name=data['name'])
        return await database.execute(query=foods.delete().where(
            foods.c.photo == food['photo']
        ))

    async def get_food(self, menu_id, name):
        return await database.fetch_one(query=foods.select().where(
            foods.c.menu_id == menu_id,
            foods.c.name == name
        ))

    async def get_food_with_id(self, food_id):
        return await database.fetch_one(query=foods.select().where(
            foods.c.id == food_id
        ))

    async def change_food_photo(self, data):
        food = await self.get_food(menu_id=data['menu_id'], name=data['name'])
        return await database.execute(query=foods.update().values(
            photo=data['photo']
        ).where(foods.c.photo == food['photo']))

class OtherSettings:
    async def get_logo(self):
        return await database.fetch_one(query=logo.select())

    async def get_about(self, lang):
        return await database.fetch_one(query=about_we.select().where(
            about_we.c.lang == lang
        ))

    async def get_stock_status(self):
        return await database.fetch_one(query=menu.select().where(
            menu.c.name_to_get == 'Aksiya'
        ))

    async def add_stock_product(self, data):
        stock = await self.get_stock_status()
        await database.execute(query=foods.insert().values(
            name=data['name_uz'],
            photo=data['photo'],
            desc=data['desc_uz'],
            price=data['price'],
            lang='uz',
            menu_id=stock['id']
        ))
        await database.execute(query=foods.insert().values(
            name=data['name_ru'],
            photo=data['photo'],
            desc=data['desc_ru'],
            price=data['price'],
            lang='ru',
            menu_id=stock['id']
        ))
        return True

    async def update_stock_status_true(self, photo):
        await database.execute(query=menu.insert().values(
            photo=photo,
            name='Aksiya',
            name_to_get='Aksiya',
            lang='uz'
        ))

        await database.execute(query=menu.insert().values(
            photo=photo,
            name='Акция',
            name_to_get='Aksiya',
            lang='ru'
        ))
    async def update_stock_status_false(self):
        return await database.execute(query=menu.delete().where(
            name_to_get='Aksiya'
        ))

    async def update_logo(self, photo):
        if await self.get_logo() is not None:
            return await database.execute(query=logo.update().values(
                photo=photo
            ))
        else:
            return await database.execute(query=logo.insert().values(
                photo=photo
            ))

    async def get_all_filials(self, lang):
        return await database.fetch_all(query=filials.select().where(filials.c.lang == lang))

    async def get_filial(self, name):
        return await database.fetch_one(query=filials.select().where(filials.c.name == name))

    async def get_all_socials(self):
        return await database.fetch_all(query=socials.select())

    async def delete_social(self, id):
        return await database.execute(query=socials.delete().where(
            socials.c.id == id
        ))

    async def add_social(self, data):
        return await database.execute(query=socials.insert().values(
            name=data['name'],
            link=data['link']
        ))

    async def add_filial(self, data):
        await database.execute(query=filials.insert().values(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            lang='uz',
            photo=data['photo'],
        ))

        await database.execute(query=filials.insert().values(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            lang='ru',
            photo=data['photo'],
        ))

    async def delete_filial(self, id):
        filial = await database.fetch_one(query=filials.select().where(
            filials.c.id == id
        ))
        return await database.execute(query=filials.delete().where(
            filials.c.latitude == filial['latitude'],
            filials.c.longitude == filial['longitude']
        ))

class BasketSettings:
    async def plus(self, product_id, user_id):
        product = await self.get_product(product_id=product_id, user_id=user_id)
        if product is None:
            await database.execute(query=basket.insert().values(
                product_id=product_id,
                quantity=1,
                user_id=user_id
            ))
            return (await self.get_product(product_id=product_id, user_id=user_id), await loader.menu.get_food_with_id(product_id))
        await database.execute(query=basket.update().values(
            quantity=int(product['quantity']) + 1,
        ))
        return (await self.get_product(product_id=product_id, user_id=user_id), await loader.menu.get_food_with_id(product_id))

    async def minus(self, product_id, user_id):
        product = await self.get_product(product_id, user_id)
        if product:
            if product['quantity'] > 1:
                await database.execute(query=basket.update().values(
                    quantity=product['quantity'] - 1
                ).where(basket.c.user_id == user_id))
                return (await self.get_product(product_id=product_id, user_id=user_id), await loader.menu.get_food_with_id(product_id), True)
            else:
                await self.remove_product(product_id=product_id, user_id=user_id)
                return 'DELETED'
        else:
            return False

    async def remove_product(self, product_id, user_id):
        return await database.execute(query=basket.delete().where(
            basket.c.user_id == user_id,
            basket.c.product_id == product_id
        ))

    async def get_user_basket(self, user_id):
        return await database.fetch_all(query=basket.select().where(
            basket.c.user_id == user_id
        ))

    async def get_product(self, product_id, user_id):
        return await database.fetch_one(query=basket.select().where(
            basket.c.product_id == product_id,
            basket.c.user_id == user_id
        ))