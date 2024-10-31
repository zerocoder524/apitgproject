import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from googletrans import Translator  # Не забудьте установить googletrans
import aiohttp

# Убедитесь, что вы правильно импортируете токен
from config import TOKENT

bot = Bot(token=TOKENT)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Определение состояний
class TranslateState(StatesGroup):
    text = State()


@dp.message(Command('send_voice'))
async def send_voice(message: Message):
    await message.answer("Введите текст, который хотите превратить в голосовое сообщение:")
    await TranslateState.text.set()  # Установить состояние


@dp.message(TranslateState.text)
async def translate_to_voice(message: Message, state: FSMContext):
    text = message.text.strip()
    translator = Translator()
    translation = translator.translate(text, dest='en').text
    await state.finish()

    async with aiohttp.ClientSession() as session:
        url = 'https://texttospeech.googleapis.com/v1/text:synthesize'
        headers = {
            'Authorization': 'Bearer ' + os.getenv('API_KEY'),  # Используйте переменную среды для API_KEY
            'Content-Type': 'application/json'
        }
        data = {
            'input': {
                'text': translation
            },
            'voice': {
                'languageCode': 'en-US',
                'name': 'en-US-Standard-A'
            },
            'audioConfig': {
                'audioEncoding': 'MP3'
            }
        }
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                audio_content = await response.json()
                audio_data = audio_content['audioContent']
                await message.answer_voice(audio_data)
            else:
                await message.answer("Произошла ошибка при преобразовании текста в речь.")


@dp.message(Command('translate_text'))
async def translate_text(message: Message):
    await message.answer("Введите текст, который хотите перевести на английский язык:")
    await TranslateState.text.set()  # Установить состояние для перевода текста


@dp.message(TranslateState.text)
async def process_translation(message: Message, state: FSMContext):
    text = message.text.strip()
    translator = Translator()
    translation = translator.translate(text, dest='en').text
    await state.finish()  # Завершить состояние
    await message.answer(translation)  # Отправить перевод пользователю


@dp.message(F.photo)
async def handle_photo(message: Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f'img/{file.file_unique_id}.jpg')
    await message.answer("Фото сохранено!")


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile("video.mp4")
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile("path_to_audio.mp3")  # Убедитесь, что вы указали путь к аудиофайлу
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/send_voice\n/handle_photo\n/video\n/audio")


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')


# @dp.message()
# async def echo_message(message: Message):
#     if message.text.lower() == "тест":
#         await message.answer("тестируем")
#     else:
#         await message.send_copy(chat_id=message.chat.id)
#
#
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':  # Исправлено на правильное имя
    asyncio.run(main())
