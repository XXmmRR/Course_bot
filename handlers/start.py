from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from keyboards.start.main_keyboard import get_start_keyboard
from filters.text_filter import Textfilter
from aiogram import F
start_router = Router(name='start router')


@start_router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer('''Привет👋🏼 Меня зовут Фрея. Я виртуальный ассистент.\n
Как тебе удобнее общаться со мной: смотреть видео сообщения или читать текст?''',
                         reply_markup=get_start_keyboard())


@start_router.message(F.content_type.in_({'photo'}) and F.caption == 'image')
async def photo_handler(message: types.Message):
    print(message.photo[-1].file_id)
    await message.answer(message.photo[-1].file_id)


@start_router.message(F.content_type.in_({'video_note', 'document'}))
async def video_handler(message: types.Message):
    print(message.video_note.file_id)
    await message.answer(message.video_note.file_id)
