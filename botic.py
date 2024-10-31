import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from googletrans import Translator
from config import TOKEN7

API_TOKEN = TOKEN7

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)  # Исправлено здесь

# Создаем экземпляр переводчика
translator = Translator()


@dp.message(Command("start", "help"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Отправь мне любой текст, и я переведу его на английский.")


@dp.message()
async def translate_text(message: types.Message):
    try:
        translated = translator.translate(message.text, dest='en')
        await message.answer(translated.text)
    except Exception as e:
        await message.answer("Произошла ошибка при переводе.")


async def main():
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
