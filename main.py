import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode

from config import TOKEN
import random
import requests

# API ключ для OpenWeatherMap
OWM_API_KEY = 'WEATHER_API_KEY'

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('photo'))
async def photo(message: Message):
  photo_list = [
    'https://img.freepik.com/free-photo/beautiful-kitten-with-colorful-clouds_23-2150752964.jpg',
    'https://img.freepik.com/free-photo/adorable-looking-kitten-with-yarn_23-2150886286.jpg',
    'https://img.freepik.com/free-photo/close-up-adorable-kitten-near-yarn_23-2150782235.jpg',
    'https://i.pinimg.com/236x/ef/bc/73/efbc73a4552228b0af41f3675104eaf3.jpg'
  ]

  rand_photo = random.choice(photo_list)
  await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.photo)
async def react_photo(message: Message):
  reaction_list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
  rand_answ = random.choice(reaction_list)
  await message.answer(rand_answ)


@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
  await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help(message:Message):
  await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather [город]")


@dp.message(CommandStart)
async def start(message: Message):
  await message.answer('Привет! Я бот!')


@dp.message(Command('weather'))
async def weather(message: Message):
  city = message.text.split(" ")[1]
  try:
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric")
    response.raise_for_status() # Проверка на ошибки HTTP
    data = response.json()

    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    description = data['weather'][0]['description']

    await message.answer(
      f"Погода в {hbold(city)}:\n"
      f"🌡️ Температура: {temp}°C\n"
      f"体感温度: {feels_like}°C\n"
      f"☁️ Описание: {description}\n"
      f"🌐 Подробнее: https://openweathermap.org/city/{data['id']}"
    )
  except requests.exceptions.RequestException as e:
    await message.answer(f"Ошибка получения данных о погоде: {e}")


async def main():
  await dp.start_polling(bot)


if __name__ == '__main__':
  asyncio.run(main())
