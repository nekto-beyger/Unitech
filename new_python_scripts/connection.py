import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import path_to_cred


# Authorize and access to API Google Sheets
gc = gspread.service_account(filename=path_to_cred)

# # Открытие таблицы по названию
# spreadsheet = gc.open("Название вашей таблицы")

# sheets = gc.openall()

# for sheet in sheets:
#     print(sheet)