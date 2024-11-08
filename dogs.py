import asyncio
import sys

# Установим SelectorEventLoop для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN7, THE_DOG_API_KEY
import requests

bot = Bot(token=TOKEN7)
dp = Dispatcher()


def get_dog_breeds():
    url = "https://api.thedogapi.com/v1/breeds"
    headers = {"x-api-key": THE_DOG_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_dog_image_by_breed(breed_id):
    url = f"https://api.thedogapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_DOG_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url'] if data else None


def get_breed_info(breed_name):
    breeds = get_dog_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Напиши мне название породы собаки, и я пришлю тебе её фото и описание.")


@dp.message()
async def send_dog_info(message: types.Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info:
        dog_image_url = get_dog_image_by_breed(breed_info['id'])
        if dog_image_url:
            info = (
                f"Порода - {breed_info['name']}\n"
#                f"Описание - {breed_info['description']}\n"
                f"Продолжительность жизни - {breed_info['life_span']} лет"
            )
            await message.answer_photo(photo=dog_image_url, caption=info)
        else:
            await message.answer("Не удалось получить изображение для этой породы.")
    else:
        await message.answer("Порода не найдена. Попробуйте еще раз.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
