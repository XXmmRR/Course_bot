from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from keyboard.start_keyboard.main_keyboard import get_main_keyboard
from filters.text_filter import Textfilter

start_router = Router(name='start router')


@start_router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer('''Привет👋🏼 Меня зовут Фрея. Я виртуальный ассистент.\n
Как тебе удобнее общаться со мной: смотреть видео сообщения или читать текст?''',
                         reply_markup=get_main_keyboard())

