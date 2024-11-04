from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Основное меню с кнопками "Привет" и "Пока"
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет")],
    [KeyboardButton(text="Пока")]
], resize_keyboard=True)

# Инлайн-кнопки с URL-ссылками
inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url='https://ria.ru/')],
    [InlineKeyboardButton(text="Музыка", url='https://music.yandex.ru/home?utmain=')],
    [InlineKeyboardButton(text="Видео", url='https://ya.ru/video/search?text=%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE')]
])

# Кнопка "Показать больше"
show_more_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data='show_more')]
])

# Инлайн-кнопки для динамических опций
dynamic_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data='option1')],
    [InlineKeyboardButton(text="Опция 2", callback_data='option2')]
])
