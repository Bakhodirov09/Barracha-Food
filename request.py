from loader import basket_settings, user_settings
from data.config import env
import requests

JOWI_API_KEY = env.str('API_KEY')
JOWI_API_SECRET = env.str('API_SECRET')
SIG = env.str('SIG')

async def send_request_to_jowi(chat_id, address, total, data):
    user = await user_settings.get_user(chat_id)
    json = {
        "api_key": JOWI_API_KEY,
        "sig": SIG,
        "restaurant_id": "3a96abba-e8be-4753-86b5-7cc57c4d49c4",

        "order": {
            "restaurant_id": "",
            "to_restaurant_id": data.get('to_restaurant_id', ""),
            "address": address,
            "phone": user['phone_number'],
            "contact": user['full_name'],
            "description": "К заказу положите приборы",
            "people_count": 0,
            "order_type": 0,
            "amount_order": total,
            "payment_method": 0,
            "payment_type": 0,
            "delivery_time": "",
            "delivery_time_type": 0,
            "delivery_price": 0,
            "discount": 0,
            "discount_sum": 0,

            "courses": [
                {
                    "course_id": "82faa070-b246-4989-acaf-3365c7d6169c",
                    "count": 1,
                    "price": 100,
                    "description": "Больше соуса"
                },
                {
                    "course_id": "ded70cb2-a96d-436b-8ef6-8917156ee82f",
                    "count": 1,
                    "price": 30,
                    "description": "Без сахара"
                }
            ]
        }
    }
    requests.request('post', 'https://api.jowi.club/v3/orders', json=json)
