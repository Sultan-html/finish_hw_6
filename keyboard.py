from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder

start_button = [
    [KeyboardButton(text='курсы валют'),KeyboardButton(text="/news"),KeyboardButton(text="/stop"),KeyboardButton(text='конвертатор валют')]
]
start_keyboard = ReplyKeyboardMarkup(keyboard=start_button, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите кнопку")



# inline_valyta = [
#     [KeyboardButton(text='USD'),
#      KeyboardButton(text='RUB'),
#      KeyboardButton(text='KZT')]
# ]
# start_asd =  ReplyKeyboardMarkup(inline_keyboard=inline_valyta, resize_keyboard=True, input_field_placeholder="Выберите кнопку")