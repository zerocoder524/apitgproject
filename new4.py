import asyncio
import sys

# Установим SelectorEventLoop для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN7
from keyboards import main_kb, inline_keyboard_test, test_keyboard, inline_keyboard_test_async, test_keyboard_inline

bot = Bot(token=TOKEN7)
dp = Dispatcher()


@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются...", show_alert=True)
    await callback.message.edit_text('Вот свежие новости!', reply_markup=await test_keyboard_inline())  # Здесь await корректен


@dp.message(F.text == 'Тестовая кнопка 1')
async def test_button(message: Message):
    await message.answer('Обработка нажатия на reply кнопку')


@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /ministraining')


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=inline_keyboard_test_async)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":  # Исправлено на '__name__'
    asyncio.run(main())
