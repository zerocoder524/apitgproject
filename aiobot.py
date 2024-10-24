import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
import asyncio
import aiohttp

from config import TOKENW, WEATHER_API_KEY  # Убедитесь, что у вас есть файл config.py с токенами

API_TOKEN = TOKENW

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
router = Router()

# Инициализация диспетчера с передачей бота
dp = Dispatcher(storage=storage)  # Передаем хранилище при создании диспетчера

# Настройка хранилища (не нужно, так как мы уже передали его в диспетчер)


# Обработчик команды /start, /help
@router.message(Command('start', 'help'))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь команду /weather <город>, чтобы получить прогноз погоды.")


@router.message(Command('weather'))
async def weather(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Пожалуйста, укажите город.")
        return

    city = args.strip()
    print(city)
    weather_data = await get_weather(city)  # Асинхронный вызов

    if weather_data:
        await message.reply(weather_data)
    else:
        await message.reply("Не удалось получить данные о погоде. Проверьте название города.")


async def get_weather(city: str) -> str:
    async with aiohttp.ClientSession() as session:  # Создаем асинхронную сессию
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        async with session.get(url) as response:  # Асинхронный запрос
            if response.status == 200:
                data = await response.json()
                city_name = data['name']
                temperature = data['main']['temp']
                weather_description = data['weather'][0]['description']
                return f"Погода в городе {city_name}:\\nТемпература: {temperature}°C\\nОписание: {weather_description.capitalize()}"
            else:
                return None


async def main():  # Оборачиваем запуск бота в асинхронную функцию
    dp.include_router(router)
    # Запускаем бота, ждем результата и обрабатываем исключения
    try:
        await dp.start_polling(bot)  # Передаем бота в start_polling
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
