import asyncio
import logging
import requests
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from bs4 import BeautifulSoup
from config import token
from keyboard import start_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

bot = Bot(token=token)
dp = Dispatcher()



class CurrencyStates(StatesGroup):
    andcurrency = State()
    amount = State()

def init_db():
    connect = sqlite3.connect('base.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news TEXT NOT NULL
        )
    ''')
    connect.commit()


@dp.message(CommandStart())
async def start_bot(message: Message):
    await message.reply("Привет", reply_markup=start_keyboard)

@dp.message(F.text == 'курсы валют')
async def start_parsing(message: Message):
    rates = await get_conversion_rates()
    await message.reply(f"Курсы валют:\n{rates}", reply_markup=start_keyboard)

@dp.message(F.text == 'конвертатор валют')
async def ask_currency(message: Message, state: FSMContext):
    await message.answer('Привет, я конвертатор валют. Выбери валюту (USD, RUB, KZT) и введи сумму для конвертации, например: USD 100.')
    await state.set_state(CurrencyStates.andcurrency)

@dp.message(State(CurrencyStates.andcurrency))
async def get_currency_and_amount(message: Message, state: FSMContext):
    try:
        currency, amount = message.text.strip().upper().split()
        amount = float(amount)
    except ValueError:
        await message.answer("Пожалуйста, укажите валюту и сумму в формате: VALUTA СУММА (например, USD 100).")
        return

    conversion_rates = await get_conversion_rates()

    if currency in conversion_rates:
        converted_amount = amount * conversion_rates[currency]
        await message.answer(f"{amount} {currency} = {converted_amount:.2f} сомов")
    else:
        await message.answer("Пожалуйста, выберите корректную валюту (USD, RUB, KZT).")
    
    await state.clear()

async def get_conversion_rates():
    response = requests.get(url='https://www.nbkr.kg/index.jsp?lang=RUS')
    soap = BeautifulSoup(response.text, 'lxml')
    
    rates = soap.find_all('td', class_='excurr')
    
    conversion_rates = {}
    if len(rates) >= 3: 
        conversion_rates['USD'] = float(rates[0].text.replace(',', '.'))
        conversion_rates['RUB'] = float(rates[1].text.replace(',', '.'))
        conversion_rates['KZT'] = float(rates[2].text.replace(',', '.'))

    return conversion_rates

@dp.message(Command('news'))
async def start_parsing_news(message: Message):
    response = requests.get(url='https://24.kg/vlast/305545_vyishlite_menya_izstranyi_azimbek_beknazarov_napisal_pismo_sadyiru_japarovu_/')
    soap = BeautifulSoup(response.text, 'lxml')
    news_items = soap.find_all('div', class_="col-sm-8 col-xs-12")

    for item in news_items:
        news_text = item.text.strip()
        await save_news(news_text)  
        await message.reply(f'{news_text}', reply_markup=start_keyboard)

async def save_news(news_text):
    connect = sqlite3.connect('base.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO news (news) VALUES (?)', (news_text,))
    connect.commit()


@dp.message(Command('stop'))
async def start_pars(message: Message):
    await message.answer('Вы остановили парсинг новостей', reply_markup=start_keyboard)

@dp.message(F.text == "Как дела?")
async def greeting(message: Message):
    await message.reply("Хорошо")

@dp.message(F.text.in_({'Привет', 'привет', 'салам'}))
async def greeting(message: Message):
    await message.answer("Привет")

async def main():
    init_db() 
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
