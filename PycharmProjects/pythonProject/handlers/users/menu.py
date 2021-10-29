from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import menu
from aiogram.dispatcher.filters import Command, Text


@dp.message_handler(Command("menu"))
async def show_menu(message:Message):
    await message.answer("Jmyakni na knopku", reply_markup=menu)


@dp.message_handler(Text(equals=["Привет", 'Kak dela', 'kak pogoda']))
async def get_answer(message: Message):
    await message.answer(f"Ты написал {Message.text}", reply_markup=ReplyKeyboardRemove())
