import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import path_to_cred
from read_variables import gsheet_id
from woocommerce import API 

# Authorize and access to API Google Sheets
gc = gspread.service_account(filename=path_to_cred)

url = "https://www.usys.co.il"
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
# Authorize and access to API Woocommerece 
wcapi = API(
    url=url,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    wp_api=True,
    version="wc/v3",
    query_string_auth=True 
)
# # # Открытие таблицы по названию
# spreadsheet = gc.open("Название вашей таблицы")
# sh = gc.open_by_key(gsheet_id)
# for sheet in sh:
#     print(sheet)

# print(gc)