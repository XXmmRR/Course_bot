from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_keyboard():
    kb = [
        [types.KeyboardButton(text="Смотреть видео👀")],
        [types.KeyboardButton(text="Читать текст 📖")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,

                                         input_field_placeholder="Выберите способ взаимодействия")
    return keyboard
