import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from config import TOKEN2
from gtts import gTTS
import os
import random

bot = Bot(token=TOKEN2)
dp = Dispatcher()


@dp.message(Command('send_voice'))
async def send_voice(message:Message):
    await message.answer("Введите текст, который хотите превратить в голосовое сообщение:")
    await TranslateState.text.set()


@dp.message(Command('handle_photo'))
async def handle_photo(message:Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f'img/{file.file_unique_id}.jpg')
    await message.answer("Фото сохранено!")


@dp.message(Command('video'))
async def video(message:Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile("video.mp4")
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))
async def audio(message:Message):
    audio = FSInputFile("")
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('training'))
async def training(message:Message):
    training_list = [
        "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини тренировка на сегодня {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.mp3")
    audio = FSInputFile('training.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove('training.mp3')


@dp.message(Command('photo', prefix='&'))
async def photo(message: Message):
    list = [
        'https://img.freepik.com/free-photo/beautiful-kitten-with-colorful-clouds_23-2150752964.jpg',
        'https://img.freepik.com/free-photo/adorable-looking-kitten-with-yarn_23-2150886286.jpg',
        'https://img.freepik.com/free-photo/close-up-adorable-kitten-near-yarn_23-2150782235.jpg',
        'https://i.pinimg.com/236x/ef/bc/73/efbc73a4552228b0af41f3675104eaf3.jpg'
    ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help(message:Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/aitext\n/react_photo\n/photo")


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')


@dp.message()
async def echo_message(message: Message):
    if message.text.lower() == "тест":
        await message.answer("тестируем")
    else:
        await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
