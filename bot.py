import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from keyboard import *
from bs4 import BeautifulSoup
from config import token
from parsing import *
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_bot(message: Message):
    await message.reply("Привет",reply_markup=start_keyboard)

@dp.message(F.text == 'курсы валют')
async def start_parsing(message: Message):
    repsonse = requests.get(url='https://www.nbkr.kg/index.jsp?lang=RUS')
    soap = BeautifulSoup(repsonse.text, 'lxml')
    cousrer = soap.find_all('div', class_='exchange-rates-body') 
    usd = soap.find_all('td', class_='excurr')
    for i in cousrer:
        print(f"{i.text}")
        await message.reply(f'{i.text}')
    await message.answer('введите ')
    await message.answer(message.text / usd)
@dp.message(Command('news'))
async def start_parsin(message: Message):
    repsonses = requests.get(url='https://24.kg/')
    soaps = BeautifulSoup(repsonses.text, 'lxml')
    cousrear = soaps.find_all('div',class_="col-xs-12")
    for item in cousrear:
            print(f"{item.text}")
            await message.reply(f'{item.text}')
@dp.message(Command('news'))
async def start_parsing_news(message: Message):
    zapros = requests.get('https://24.kg/') 
    if zapros.status == 200:
                soaps = BeautifulSoup(await zapros.text(), 'lxml')
                cousrear = soaps.find_all('div', class_="col-xs-12")
                for item in cousrear:
                    print(f"{item.text}")
                    await message.reply(f'{item.text}')
    else:
                await message.reply("Ошибка при получении новостей.")

@dp.message(F.text == "Как дела?")
async def greeting(message: Message):
    await message.reply("Хорошо")

@dp.message(F.text.in_({'Привет', 'привет', 'салам'}))
async def greeting(message: Message):
    await message.answer("Привет")

@dp.message()
async def echo(message: Message):
    await message.answer("Я вас не понял")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")