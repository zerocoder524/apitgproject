import asyncio
import sys

# Установим SelectorEventLoop для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN7
import keyboards4 as kb

bot = Bot(token=TOKEN7)
dp = Dispatcher()

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

@dp.message(Command('dynamic'))
async def dynamic_command(message: Message):
    await message.answer("Нажмите на кнопку, чтобы показать больше", reply_markup=kb.show_more_button)

@dp.callback_query(F.data == 'show_more')
async def show_more_options(callback: CallbackQuery):
    await callback.answer()  # Убираем сообщение о нажатии
    await callback.message.edit_text("Выберите опцию:", reply_markup=kb.dynamic_options)

@dp.callback_query(F.data == 'option1')
async def option1_selected(callback: CallbackQuery):
    await callback.answer()  # Убираем сообщение о нажатии
    await callback.message.answer("Вы выбрали Опцию 1!")

@dp.callback_query(F.data == 'option2')
async def option2_selected(callback: CallbackQuery):
    await callback.answer()  # Убираем сообщение о нажатии
    await callback.message.answer("Вы выбрали Опцию 2!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
