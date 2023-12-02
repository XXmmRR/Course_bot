import gspread
from google.oauth2.service_account import Credentials

# Используйте свой путь к файлу с учетными данными
path_to_credentials = '/home/q/PycharmProjects/course_bot/gspread_utils/owner-bot-bfdb3307dfa1.json'

# Области доступа
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Аутентификация
creds = Credentials.from_service_account_file(path_to_credentials, scopes=scopes)
client = gspread.authorize(creds)

# Открытие таблицы по названию
spreadsheet = client.open("Админка Бота общая")

# Выбор листа
sheet = spreadsheet.worksheet('Owner-Bot')
