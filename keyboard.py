from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder

start_button = [
    [KeyboardButton(text='курсы валют'),KeyboardButton(text="/news"),KeyboardButton(text="/stop")]
]
start_keyboard = ReplyKeyboardMarkup(keyboard=start_button, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите кнопку")
