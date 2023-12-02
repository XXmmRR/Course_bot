from aiogram import types
from gspread_utils.buttons.get_main_buttons import get_main_keyboard_fields
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    [builder.add(types.KeyboardButton(text=x)) for x in get_main_keyboard_fields()]
    builder.adjust(2)
    keyboard = types.ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True,
                                         input_field_placeholder="Главное меню")
    return keyboard

