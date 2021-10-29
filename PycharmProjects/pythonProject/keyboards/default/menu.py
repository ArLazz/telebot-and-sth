from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Привет"),
        ],
        [
            KeyboardButton(text='Kak dela'),
            KeyboardButton(text='kak pogoda')
        ],
    ],
    resize_keyboard=True
)
