import asyncio
import sys

# Установим SelectorEventLoop для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN7, NASA_API_KEY
import requests
import random
from datetime import datetime, timedelta

bot = Bot(token=TOKEN7)
dp = Dispatcher()


def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
    response = requests.get(url)
    return response.json()


@dp.message(Command("random_apod"))
async def random_apod(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']

    await message.answer_photo(photo=photo_url, caption=f"{title}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
