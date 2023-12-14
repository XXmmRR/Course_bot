from gspread_utils.google_client import sheet


def get_text(sheet=sheet, col_id=3):
    texts = []          # Список для текстов вопросов
    keyboards = []      # Список для наборов клавиатур (ответов)
    actions = []        # Список для наборов действий, соответствующих каждому набору клавиатур

    temp_keyboard = []  # Временный список для сбора ответов текущего вопроса
    temp_actions = []   # Временный список для сбора действий текущего вопроса
    current_index = 1

    for row in sheet.get_all_values():
        # Проверяем, является ли строка началом нового вопроса
        if row[3] != '' and row[3] != '-' or row[0].isdigit():
            if row[0] == 'Вопрос ':
                texts.append(row[3])
            elif row[0].startswith('Ответ') and texts:
                temp_keyboard.append(row[col_id])

            # Если строка является следствием выбора, собираем её во временный список действий
            elif row[0].startswith('Следствие выбора') and texts:
                temp_actions.append(row[col_id])
            if row[0].isdigit() and int(row[0]) != current_index:
                if temp_keyboard:
                    keyboards.append(temp_keyboard.copy())
                if temp_actions:
                    actions.append(temp_actions.copy())
                temp_actions.clear()
                temp_keyboard.clear()
                current_index += 1

    return texts, keyboards, actions


print(get_text())