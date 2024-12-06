import logging

from aiogram import Bot, executor, types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from  config import *
import  texts
from  keyboards import *
logging.basicConfig(level = logging.INFO)
bot = Bot(token = API)
dp = Dispatcher(bot, storage= MemoryStorage())

@dp.message_handler(commands = ["start"])
async def start(message):
    await message.answer(texts.start, reply_markup = start_kb)

@dp.message_handler(text ='О магазине')
async def price(message):
    await message.answer(texts.about, reply_markup = start_kb)

@dp.message_handler(text = 'Цена')
async def info(message):
    await message.answer('Что желаем?', reply_markup = catalog_kb)

@dp.callback_query_handler(text='Успешница')
async def buy_1(call):
    await call.message.answer(texts.dall_1, reply_markup=buy_kb)
    await call.answer()
@dp.callback_query_handler(text='Подорожница')
async def buy_2(call):
    await call.message.answer(texts.dall_2, reply_markup=buy_kb)
    await call.answer()
@dp.callback_query_handler(text='Ведучка')
async def buy_3(call):
    await call.message.answer(texts.dall_3, reply_markup=buy_kb)
    await call.answer()

@dp.callback_query_handler(text='Другие')
async def buy_4(call):
    await call.message.answer(texts.other, reply_markup=buy_kb)
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
