import asyncio
import sys

# Установим SelectorEventLoop для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN7, THE_CAT_API_KEY, THE_DOG_API_KEY
import requests
import keyboards5 as kb

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


def get_dog_breed_info(breed_name):
    breeds = get_dog_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None


def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url'] if data else None


def get_cat_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.main_kb)


@dp.message(F.text == "Привет")
async def hello_command(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


@dp.message(F.text == "Пока")
async def goodbye_command(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")


@dp.message(Command('links'))
async def links_command(message: Message):
    await message.answer("Выберите один из ресурсов:", reply_markup=kb.inline_keyboard_test)


@dp.message(Command('pets'))
async def dynamic_command(message: Message):
    await message.answer("Нажмите на кнопку, чтобы показать больше", reply_markup=kb.show_more_button)


@dp.callback_query(F.data == 'show_more')
async def show_more_options(callback: CallbackQuery):
    await callback.answer()  # Убираем сообщение о нажатии
    await callback.message.edit_text("Сделайте выбор:", reply_markup=kb.dynamic_options)


@dp.callback_query(F.data == 'option1')
async def option1_selected(callback: CallbackQuery):
    await callback.answer()  # Убираем сообщение о нажатии
    await callback.message.answer("Введите название породы кошки:")


@dp.callback_query(F.data == 'option2')
async def option2_selected(callback: CallbackQuery):
    await callback.answer()  # Убираем сообщение о нажатии
    await callback.message.answer("Введите название породы собаки:")


@dp.message(F.text)
async def breed_info_request(message: Message):
    # Проверяем, является ли сообщение запросом информации о породе
    dog_info = get_dog_breed_info(message.text)
    cat_info = get_cat_breed_info(message.text)

    if dog_info:
        await message.answer(f"Информация о породе собаки '{dog_info['name']}'")
        dog_image_url = get_dog_image_by_breed(dog_info['id'])
        if dog_image_url:
            await message.answer(dog_image_url)
    elif cat_info:
        await message.answer(f"Информация о породе кошки '{cat_info['name']}':\n{cat_info['description']}")
        cat_image_url = get_cat_image_by_breed(cat_info['id'])
        if cat_image_url:
            await message.answer(cat_image_url)
    else:
        await message.answer("Порода не найдена. Пожалуйста, попробуйте еще раз.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
