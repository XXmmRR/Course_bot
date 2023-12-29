from gspread_utils.google_client import sheet
from gspread_utils.text.texts import get_text

def get_main_keyboard_fields(sheet=sheet):
    # Читаем вторую строку (индексация начинается с 1)
    row_values = sheet.row_values(2)

    seen = set()
    unique_values = [value for value in row_values[1:] if len(value) > 10 and value not in seen and not seen.add(value)]

    return unique_values


def get_work_buttons(search_text, worksheet=sheet):
    """
    Поиск и извлечение данных из Google Sheets до последнего заполненного поля.

    :param search_text: Текст для поиска во второй строке.
    :param worksheet: Объект Worksheet для взаимодействия с таблицами в gspread.
    :return: Данные из соответствующих ячеек в третьей строке, исключая пустые.
    """

    # Получение данных второй строки
    second_row_values = worksheet.row_values(2)

    # Получение данных третьей строки
    third_row_values = worksheet.row_values(3)

    # Поиск и извлечение данных
    for i, value in enumerate(second_row_values):
        if search_text in value:
            # Извлечение данных из третьей строки, начиная с третьего столбца
            data = third_row_values[i+2:] if i+2 < len(third_row_values) else []
            # Удаление пустых элементов
            return [item for item in data if item]
    return None

def get_column_id_by_text(search_text, worksheet=sheet):
    """
    Поиск заданного текста в третьей строке и возвращение номера колонки.

    :param search_text: Текст для поиска в третьей строке.
    :param worksheet: Объект Worksheet для взаимодействия с таблицами в gspread.
    :return: Номер колонки, где был найден текст.
    """

    # Получение данных третьей строки
    third_row_values = worksheet.row_values(3)

    # Поиск текста и возвращение номера колонки
    for i, value in enumerate(third_row_values):
        if search_text in value:
            # Возвращение номера колонки (индексация начинается с 1)
            return i
    return None


id = (get_column_id_by_text('Общее'))
print(get_text(col_id=id-1))