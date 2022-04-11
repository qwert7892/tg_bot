import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import logging

from db_code import User

TOKEN = '5188646732:AAGPy070CBC5RFxVvoiE0ch1T7OdoFcWBuU'

logging.basicConfig(level=logging.INFO)

user = None
profile_list = []

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Перед знакомствами \n заполните профиль \n чтоб продолжить напишите /profile")


@dp.message_handler(commands=['profile'])
async def profile_fill(message: types.Message):
    global user
    global profile_list
    await message.reply('Enter the name')
    # profile_fill_name(message)

    # @dp.message_handler
    # async def profile_fill_name(message: types.Message):
    #    global profile_list
    profile_list.append(message.text)
    print(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
