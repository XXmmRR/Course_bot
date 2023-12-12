from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from keyboards.main.main_keyboard import get_main_menu_keyboard, get_keyboard_by_list
from filters.text_filter import Textfilter
from gspread_utils.buttons.get_main_buttons import get_main_keyboard_fields
from gspread_utils.text.texts import get_text


menu_router = Router(name='menu router')

fiedls = get_main_keyboard_fields()
company_texts = get_text()


@menu_router.message(Textfilter('Читать текст 📖'))
async def read_text(message: types.Message):
    keyboard = get_main_menu_keyboard()
    await message.answer('Что тебя интересует сейчас? 🤔', reply_markup=keyboard)


@menu_router.message(Textfilter('Смотреть видео👀'))
async def watch_video(message: types.Message):
    await message.answer('Not implemented')


@menu_router.message(Textfilter(fiedls[0]))
async def about_company_main(message: types.Message):
    await message.answer(company_texts[0][0], reply_markup=get_keyboard_by_list(keyboard_list=company_texts[1][0]))
