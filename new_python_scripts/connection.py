import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import path_to_cred
from read_variables import gsheet_id

# Authorize and access to API Google Sheets
gc = gspread.service_account(filename=path_to_cred)


# # # Открытие таблицы по названию
# spreadsheet = gc.open("Название вашей таблицы")
# sh = gc.open_by_key(gsheet_id)
# for sheet in sh:
#     print(sheet)

# print(gc)