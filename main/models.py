import uuid
from sqlalchemy import Table, String, Column, Integer, Boolean, BigInteger, DateTime, ForeignKey, Text, Uuid, Float, \
    Select, Enum
from main.database_settings import metadata


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('full_name', String),
    Column('phone_number', String),
    Column('username', String),
    Column('chat_id', BigInteger),
    Column('status', Boolean, default=True),
    Column('time', DateTime, nullable=True),
    Column('days', Integer, nullable=True),
    Column('lang', String),
)

admins = Table(
    "admins",
    metadata,
    Column("id", Integer, primary_key=True),
    Column('chat_id', BigInteger)
)

menu = Table(
    "menu",
    metadata,
    Column("id", Integer, primary_key=True),
    Column('photo', String),
    Column('name', String),
    Column('name_to_get', String),
    Column('lang', String),
)

basket = Table(
    'basket',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('product_id', Integer, ForeignKey('foods.id', ondelete='CASCADE')),
    Column('quantity', Integer),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'))
)

foods = Table(
    'foods',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('menu_id', Integer, ForeignKey("menu.id", ondelete='CASCADE'), nullable=True),
    Column("name", String),
    Column("price", Integer),
    Column("desc", Text),
    Column("photo", Text),
    Column("lang", String),
    Column('created_at', DateTime(timezone=True)),
    Column('updated_at', DateTime(timezone=True))
)

filials = Table(
    'filials',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('lang', String),
    Column('photo', String),
)

socials = Table(
    'socials',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('link', String),
)

locations = Table(
    'locations',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('latitude', String),
    Column('longitude', String),
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete='CASCADE')),
)

order_abouts = Table(
    'order_abouts',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('number_uuid', Uuid, default=uuid.uuid4, unique=True),
    Column('number_id', BigInteger),
    Column('total', BigInteger),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('date', DateTime),
    Column('where_to', String, nullable=True),
    Column('which_filial', String, nullable=True),
    Column('type', String)
)

history_buys = Table(
    'history_buys',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('number_id', Integer, ForeignKey('order_abouts.id', ondelete='CASCADE')),
    Column('food_id', Integer),
    Column('quantity', Integer),
)

logo = Table(
    'logo',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('photo', String)
)

about_we = Table(
    'about_we',
    metadata,
    Column('id', Integer),
    Column('about', String),
    Column('lang', String)
)