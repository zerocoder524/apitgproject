import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://img.freepik.com/free-photo/beautiful-kitten-with-colorful-clouds_23-2150752964.jpg', 'https://img.freepik.com/free-photo/adorable-looking-kitten-with-yarn_23-2150886286.jpg', 'https://img.freepik.com/free-photo/close-up-adorable-kitten-near-yarn_23-2150782235.jpg', 'https://i.pinimg.com/236x/ef/bc/73/efbc73a4552228b0af41f3675104eaf3.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)


@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help(message:Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/aitext\n/react_photo\n/photo")


@dp.message(CommandStart)
async def start(message: Message):
    await message.answer('Привет! Я бот!')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
