from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from keyboards.main.main_keyboard import get_main_menu_keyboard, get_keyboard_by_list
from filters.text_filter import Textfilter
from gspread_utils.buttons.get_main_buttons import get_main_keyboard_fields
from gspread_utils.text.texts import get_text
from states.menu_routing_states import FollowHandlers
from aiogram.fsm.context import FSMContext
from gspread_utils.constants import ABOUT_COMPANY_ID, FEED_BACK_ID, PARTNER_ID
from states.menu_states import FeedBackDynamicStates, PartnerDynamicStates

menu_router = Router(name='menu router')

fiedls = get_main_keyboard_fields()
company_texts = get_text(col_id=ABOUT_COMPANY_ID)
contact_texts = get_text(col_id=FEED_BACK_ID)
work_texts = get_text(col_id=PARTNER_ID)


@menu_router.message(Textfilter('Читать текст 📖'))
async def read_text(message: types.Message):
    keyboard = get_main_menu_keyboard()
    await message.answer('Что тебя интересует сейчас? 🤔', reply_markup=keyboard)


@menu_router.message(Textfilter('Смотреть видео👀'))
async def watch_video(message: types.Message):
    await message.answer('Not implemented')


@menu_router.message(Textfilter(fiedls[0]))
async def about_company_main(message: types.Message, state: FSMContext):
    await state.clear()
    await split_and_send_message(company_texts[0][0], reply_markup=get_keyboard_by_list(keyboard_list=company_texts[1][0]))
    await state.set_state(FollowHandlers.first_handler)


@menu_router.message(Textfilter(fiedls[1]))
async def contacts_main(message: types.Message, state: FSMContext):
    await state.clear()
    await split_and_send_message(contact_texts[0][0], reply_markup=get_keyboard_by_list(keyboard_list=contact_texts[1][0]))
    await state.set_state(FollowHandlers.second_handler)


@menu_router.message(Textfilter(fiedls[2]))
async def work_main(message: types.Message, state: FSMContext):
    await split_and_send_message(work_texts[0][0], reply_markup=get_keyboard_by_list(keyboard_list=work_texts[1][0]))
    await state.clear()
    await state.set_state(FollowHandlers.third_handler)


@menu_router.message(FollowHandlers.third_handler)
async def handle_message_second(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    current_index = user_data.get('current_index', 0)  # Получаем текущий индекс, начинаем с 0
    current_state_index = user_data.get('state_index', 1)
    print('Да я тууут')
    texts, keyboards, actions = get_text(col_id=PARTNER_ID)  # Получаем данные

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
            await state.set_state(FollowHandlers.third_handler)
            await state.update_data(current_index=current_index)
            return
        elif action == 'В меню':
            await read_text(message)
            await state.clear()
            return

        # Сохраняем обновлённый индекс текущего вопроса в состоянии
        await state.update_data(current_index=current_index)

        # Отправляем следующий текст
        if current_index <= len(texts):
            await split_and_send_message(texts[current_index], reply_markup=get_keyboard_by_list(keyboards[current_index]))
    else:
        if current_index <= len(texts):
            await split_and_send_message(texts[current_index], reply_markup=get_keyboard_by_list(keyboards[current_index]))


@menu_router.message(FollowHandlers.second_handler)
async def handle_message_second(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    current_index = user_data.get('current_index', 0)  # Получаем текущий индекс, начинаем с 0

    texts, keyboards, actions = get_text(col_id=FEED_BACK_ID)  # Получаем данные
    print('я тут')
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
        print(action)
        if action == 'Следующий вопрос':
            # Убедитесь, что индекс не выходит за рамки списка
            if current_index + 1 < len(texts):
                current_index += 1  # Переходим к следующему вопросу
        elif action == 'Свободный ввод текста и сдедующий вопрос':
            await message.answer('Введите текст', reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(FollowHandlers.second_handler)
            return
        elif action == 'В меню':
            await read_text(message)
            await state.clear()
            return
        else:
            # Здесь может быть ваша логика для завершения диалога или цикла вопросов
            await message.answer("Вы достигли конца диалога.")


        # Сохраняем обновлённый индекс текущего вопроса в состоянии
        await state.update_data(current_index=current_index)

        # Отправляем следующий текст
        if current_index <= len(texts):
            print(current_index)
            await split_and_send_message(texts[current_index], reply_markup=get_keyboard_by_list(keyboards[current_index]))


@menu_router.message(FollowHandlers.first_handler)
async def handle_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    current_index = user_data.get('current_index', 0)  # Получаем текущий индекс, начинаем с 0

    texts, keyboards, actions = get_text(col_id=ABOUT_COMPANY_ID)  # Получаем данные

    normalized_message_text = message.text.strip().lower()
    normalized_keyboard_options = [option.strip().lower() for option in keyboards[current_index]]

    if normalized_message_text in normalized_keyboard_options:
        choice_index = normalized_keyboard_options.index(normalized_message_text)
        action = actions[current_index][choice_index]

        if action == 'Следующий вопрос':
            if current_index + 1 < len(texts):
                current_index += 1
            else:
                await split_and_send_message(message, texts[current_index])
                await state.clear()
                return
        elif action == 'В меню':
            await split_and_send_message(message, texts[current_index])
            await state.clear()
            return

        await state.update_data(current_index=current_index)

        if current_index < len(texts):
            await split_and_send_message(message, texts[current_index], get_keyboard_by_list(keyboards[current_index]))
    else:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов ответов.")


async def split_and_send_message(message, text, reply_markup=None):
    # Разделяем текст по символу переноса строки и отправляем каждую часть отдельным сообщением
    for part in text.split('\n'):
        await message.answer(part, reply_markup=reply_markup)