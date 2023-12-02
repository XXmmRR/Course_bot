from aiogram import types


def get_main_keyboard():
    kb = [
        [types.KeyboardButton(text="Смотреть видео👀")],
        [types.KeyboardButton(text="Читать текст 📖")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         input_field_placeholder="Выберите способ взаимодействия")
    return keyboard
