import sqlalchemy
from sqlalchemy import DateTime
from main.database_settings import metadata

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('full_name', sqlalchemy.String),
    sqlalchemy.Column('phone_number', sqlalchemy.String),
    sqlalchemy.Column('chat_id', sqlalchemy.BigInteger),
    sqlalchemy.Column('lang', sqlalchemy.String),
)

admins = sqlalchemy.Table(
    "admins",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('chat_id', sqlalchemy.BigInteger)
)

menu = sqlalchemy.Table(
    "menu",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('photo', sqlalchemy.String),
    sqlalchemy.Column('name', sqlalchemy.String),
)

foods = sqlalchemy.Table(
    'foods',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('menu_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("menu.id")),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column("desc", sqlalchemy.Text),
    sqlalchemy.Column("photo", sqlalchemy.Text),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime(timezone=True)),
    sqlalchemy.Column('updated_at', sqlalchemy.DateTime(timezone=True))
)

filials = sqlalchemy.Table(
    'filials',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('latitude', sqlalchemy.String),
    sqlalchemy.Column('longitude', sqlalchemy.String),
)

order_numbers = sqlalchemy.Table(
    'order_numbers',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('number', sqlalchemy.BigInteger)
)

history_buys = sqlalchemy.Table(
    'history_buys',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('chat_id', sqlalchemy.BigInteger),
    sqlalchemy.Column('number_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('order_numbers.id')),
    sqlalchemy.Column('food_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('foods.id')),
    sqlalchemy.Column('quantity', sqlalchemy.Integer)
)
