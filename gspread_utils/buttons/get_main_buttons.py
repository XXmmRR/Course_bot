from gspread_utils.google_client import sheet


def get_main_keyboard_fields(sheet=sheet):
    # Читаем вторую строку (индексация начинается с 1)
    row_values = sheet.row_values(2)

    seen = set()
    unique_values = [value for value in row_values[1:] if len(value) > 10 and value not in seen and not seen.add(value)]

    return unique_values
