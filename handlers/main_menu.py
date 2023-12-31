from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from keyboards.main.main_keyboard import get_main_menu_keyboard, get_keyboard_by_list
from filters.text_filter import Textfilter
from gspread_utils.buttons.get_main_buttons import get_main_keyboard_fields, get_column_id_by_text, \
    get_column_by_menu_second_row, get_work_buttons
from gspread_utils.text.texts import get_text
from states.menu_routing_states import FollowHandlers
from aiogram.fsm.context import FSMContext
from gspread_utils.constants import ABOUT_COMPANY_ID, FEED_BACK_ID, PARTNER_ID
from states.menu_states import FeedBackDynamicStates, PartnerDynamicStates
from aiogram.types import PhotoSize, InputMediaPhoto

menu_router = Router(name='menu router')

fiedls = get_main_keyboard_fields()
company_texts = get_text(col_id=ABOUT_COMPANY_ID)
contact_texts = get_text(col_id=FEED_BACK_ID)
work_texts = get_text(col_id=PARTNER_ID)


@menu_router.message(Textfilter('Читать текст 📖'))
async def read_text(message: types.Message, state: FSMContext):
    keyboard = get_main_menu_keyboard()
    await message.answer('Что тебя интересует сейчас? 🤔', reply_markup=keyboard)
    await state.update_data({'video_mode': 0})
    await state.set_state(FollowHandlers.first_handler)


@menu_router.message(Textfilter('Смотреть видео👀'))
async def watch_video(message: types.Message, state: FSMContext):
    keyboard = get_main_menu_keyboard()
    await message.answer('Что тебя интересует сейчас? 🤔', reply_markup=keyboard)
    await state.update_data({'video_mode': 1})
    await state.set_state(FollowHandlers.first_handler)


@menu_router.message(Textfilter(fiedls[3]))
async def work(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer('Кем ты хочешь стать 🚀', reply_markup=get_keyboard_by_list(get_work_buttons('Трудоустройство 🚀')))
    await state.set_state(FollowHandlers.work_handler)


@menu_router.message(FollowHandlers.work_handler)
async def works_questions(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    video_mod = user_data.get('video_mode')
    if not user_data.get('first_message'):
        await state.set_data(
            {
                'first_message': message.text,
                'video_mode': video_mod
             }
        )
    user_data = await state.get_data()
    current_index = user_data.get('current_index', 0)  # Получаем текущий индекс, начинаем с 0
    first_message = user_data.get('first_message')
    col_id = get_column_id_by_text(search_text=first_message)
    is_video_mode = user_data.get('video_mode')
    print(is_video_mode)
    texts, keyboards, actions, pictures, videos = get_text(col_id=col_id)
    print(pictures)
    # Нормализуем текст сообщения, удаляем пробелы и приводим к нижнему регистру
    normalized_message_text = message.text.strip().lower()

    # Нормализуем варианты клавиатуры, тоже удаляем пробелы и приводим к нижнему регистру
    normalized_keyboard_options = [option.strip().lower() for option in keyboards[current_index]]

    # Проверяем, совпадает ли нормализованный текст сообщения с одной из нормализованных опций клавиатуры
    if normalized_message_text in normalized_keyboard_options:
        # Получаем индекс выбранной опции ответа
        choice_index = normalized_keyboard_options.index(normalized_message_text)
        # Получаем соответствующее действие
        action = actions[current_index][choice_index]

        if action == 'Следующий вопрос':
            # Убедитесь, что индекс не выходит за рамки списка
            if current_index + 1 < len(texts):
                current_index += 1  # Переходим к следующему вопросу
            else:
                # Здесь может быть ваша логика для завершения диалога или цикла вопросов
                await message.answer("Вы достигли конца диалога.")
        elif action == 'Свободный ввод текста и сдедующий вопрос':
            current_index += 1
            await message.answer('Введите текст', reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(FollowHandlers.work_handler)
            await state.update_data(current_index=current_index)
            return
        elif action == 'В меню':
            await state.clear()
            await read_text(message, state)
            return

        # Сохраняем обновлённый индекс текущего вопроса в состоянии
        await state.update_data(current_index=current_index)

        # Отправляем следующий текст
        if current_index <= len(texts):
            if not is_video_mode:
                try:
                    pic = pictures[current_index]
                    await split_and_send_message(message, texts[current_index], pic=pic,
                                                 reply_markup=get_keyboard_by_list(keyboards[current_index]))
                except:
                    await split_and_send_message(message, texts[current_index],
                                                 reply_markup=get_keyboard_by_list(keyboards[current_index]))
            else:
                await message.answer_video_note(video_note=videos[current_index])
    else:
        if current_index <= len(texts):
            if not is_video_mode:
                try:
                    pic = pictures[current_index]
                    await split_and_send_message(message, texts[current_index], pic=pic,
                                                 reply_markup=get_keyboard_by_list(keyboards[current_index]))
                except:
                    await split_and_send_message(message, texts[current_index],
                                                 reply_markup=get_keyboard_by_list(keyboards[current_index]))
            else:
                await message.answer_video_note(video_note=videos[current_index],
                                                reply_markup=get_keyboard_by_list(keyboards[current_index]))


@menu_router.message(FollowHandlers.first_handler)
async def handle_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    video_mod = user_data.get('video_mode')
    if not user_data.get('first_message'):
        await state.set_data(
            {
                'first_message': message.text,
                'video_mode': video_mod
             }
        )
    user_data = await state.get_data()
    current_index = user_data.get('current_index', 0)  # Получаем текущий индекс, начинаем с 0
    first_message = user_data.get('first_message')
    if first_message == 'Трудоустройство 🚀':
        await work(message, state)
    col_id = get_column_by_menu_second_row(search_text=first_message)
    is_video_mode = user_data.get('video_mode')
    print(is_video_mode)
    texts, keyboards, actions, pictures, videos = get_text(col_id=col_id)
    # Нормализуем текст сообщения, удаляем пробелы и приводим к нижнему регистру
    normalized_message_text = message.text.strip().lower()

    # Нормализуем варианты клавиатуры, тоже удаляем пробелы и приводим к нижнему регистру
    normalized_keyboard_options = [option.strip().lower() for option in keyboards[current_index]]

    # Проверяем, совпадает ли нормализованный текст сообщения с одной из нормализованных опций клавиатуры
    if normalized_message_text in normalized_keyboard_options:
        # Получаем индекс выбранной опции ответа
        choice_index = normalized_keyboard_options.index(normalized_message_text)
        # Получаем соответствующее действие
        action = actions[current_index][choice_index]

        if action == 'Следующий вопрос':
            # Убедитесь, что индекс не выходит за рамки списка
            if current_index + 1 < len(texts):
                current_index += 1  # Переходим к следующему вопросу
            else:
                # Здесь может быть ваша логика для завершения диалога или цикла вопросов
                await message.answer("Вы достигли конца диалога.")
        elif action == 'Свободный ввод текста и сдедующий вопрос':
            current_index += 1
            await message.answer('Введите текст', reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(FollowHandlers.first_handler)
            await state.update_data(current_index=current_index)
            return
        elif action == 'В меню':
            await state.clear()
            await read_text(message, state)
            return
        elif action.startswith(' Переход на ветку ='):
            splited_action = action.split('=')[-1].strip()
            if splited_action == 'Трудоустройство 🚀':
                await work(message, state)
                return
            await state.set_data({'first_message': splited_action})
            await handle_message(message, state)
            return
        # Сохраняем обновлённый индекс текущего вопроса в состоянии
        await state.update_data(current_index=current_index)

        # Отправляем следующий текст
        if current_index <= len(texts):
            if not is_video_mode:
                try:
                    pic = pictures[current_index]
                    await split_and_send_message(message, texts[current_index], pic=pic, reply_markup=get_keyboard_by_list(keyboards[current_index]))
                except:
                    await split_and_send_message(message, texts[current_index], reply_markup=get_keyboard_by_list(keyboards[current_index]))
            else:
                await message.answer_video_note(video_note=videos[current_index], reply_markup=get_keyboard_by_list(keyboards[current_index]))
    else:
        if current_index <= len(texts):
            if not is_video_mode:
                try:
                    pic = pictures[current_index]
                    await split_and_send_message(message, texts[current_index], pic=pic, reply_markup=get_keyboard_by_list(keyboards[current_index]))
                except:
                    await split_and_send_message(message, texts[current_index], reply_markup=get_keyboard_by_list(keyboards[current_index]))
            else:
                await message.answer_video_note(video_note=videos[current_index], reply_markup=get_keyboard_by_list(keyboards[current_index]))


async def split_and_send_message(message, text, pic=None, reply_markup=None):
    # Разделяем текст по символу переноса строки
    parts = text.split(r'\n')

    # Проверяем, есть ли картинка для отправки
    if pic:
        # Если есть картинка, отправляем первую часть сообщения с картинкой
        if parts[0] != '\n':
            await message.answer_photo(photo=pic, caption=parts[0], reply_markup=reply_markup, parse_mode='HTML')
        # Удаляем первую часть, так как она уже отправлена
        parts = parts[1:]
    # Далее отправляем оставшиеся части сообщения
    for part in parts:
        if part != '\n':
            await message.answer(part, reply_markup=reply_markup, parse_mode='HTML')