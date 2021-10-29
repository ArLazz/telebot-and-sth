from main import bot, dp

from aiogram.types import Message
from config import admin_id


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


@dp.message_handler()
async def echo(message: Message):
    if message.text == "привет":
        await message.answer(text="привет")
    else:
        text = f"Ты написал:'{message.text}'"
        await message.answer(text=text)
