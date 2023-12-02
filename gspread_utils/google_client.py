import gspread
from google.oauth2.service_account import Credentials

# Используйте свой путь к файлу с учетными данными
path_to_credentials = 'owner-bot-bfdb3307dfa1.json'

# Области доступа
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Аутентификация
creds = Credentials.from_service_account_file(path_to_credentials, scopes=scopes)
client = gspread.authorize(creds)

# Открытие таблицы по названию
spreadsheet = client.open("Админка Бота общая")

# Выбор листа
sheet = spreadsheet.sheet1

# Чтение данных из таблицы
data = sheet.get_all_values()

# Выводим данные
for row in data:
    print(row)
