from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from keyboard.start_keyboard.main_keyboard import get_main_keyboard
from filters.text_filter import Textfilter

menu_router = Router(name='menu router')


@menu_router.message(Textfilter('Читать текст 📖'))
async def read_text(message: types.Message):
    await message.answer('Что тебя интересует сейчас? 🤔')


@menu_router.message(Textfilter('Смотреть видео👀'))
async def watch_video(message: types.Message):
    await message.answer('Not implemented')
