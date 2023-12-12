from gspread_utils.google_client import sheet


def get_text(sheet=sheet, col_id=3):
    texts = []
    keyboards = []
    temp_keyboard = []
    temp_actions = []
    actions = []

    old_count = 0
    current_count = 0
    for i in sheet.get_all_values():
        if i[0] == 'Вопрос ':
            current_count += 1
            if i[3] != '' and i[3] != '-':
                texts.append(i[3])
        if i[0].startswith('Ответ'):
            if i[3] != '' and i[3] != '-':
                if current_count - 1 == old_count:
                    temp_keyboard.append(i[3])
                else:
                    old_count += 1
                    keyboards.append(temp_keyboard.copy())
                    temp_keyboard.clear()
                    temp_keyboard.append(i[3])
        if i[0].startswith('Следствие выбора'):
            if i[3] != '' and i[3] != '-':
                if current_count - 1 == old_count:
                    temp_actions.append(i[3])
                else:
                    old_count += 1
                    actions.append(temp_actions.copy())
                    temp_actions.clear()
                    temp_actions.append(i[3])



    return texts, keyboards
