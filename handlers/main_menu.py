from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from keyboards.main.main_keyboard import get_main_menu_keyboard
from filters.text_filter import Textfilter

menu_router = Router(name='menu router')


@menu_router.message(Textfilter('Читать текст 📖'))
async def read_text(message: types.Message):
    keyboard = get_main_menu_keyboard()
    await message.answer('Что тебя интересует сейчас? 🤔', reply_markup=keyboard)


@menu_router.message(Textfilter('Смотреть видео👀'))
async def watch_video(message: types.Message):
    await message.answer('Not implemented')
