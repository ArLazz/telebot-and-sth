import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "1214104407:AAH-TV6IR0kEt6rmOqAmNtlPOhqP1g0KhhA"

admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
