# from connection import gc
# from read_variables import your_token, api_endpoint, gsheet_id

# sh = gc.open(gsheet_id)  # The name of your Google Sheets document
# for sheet in sh:

# # Retrieving values from column B
#     column_b_values = sheet.col_values(2)  # gspread indexes columns and rows starting from 1
#     item_ids_to_rows_map = {}
#     for index, value in enumerate(column_b_values, start=1):
#         value = value.strip()
#         if len(value) >= 5 and value.isdigit():
#             item_ids_to_rows_map[value] = index

#     item_ids = list(item_ids_to_rows_map.keys())
#     if not item_ids:
#         print("No valid item IDs found in column B.")
    
# print(item_ids)

from get_data_from_gsheet import get_data_from_gsheet
from get_data_from_website import get_data_from_website, get_all_products
from connection import wcapi
import pandas as pd

response = wcapi.get("products")

if response.status_code == 200:
    products = get_all_products()
    website_data = get_data_from_website(products)
else:
    print(f"Error: {response.status_code}")
    products = []
    
gsheet_data = get_data_from_gsheet()

# print('google sheets:')
# print(gsheet_data.info())
# print()
# print('website:')
# print(website_data.info())

common_cols = gsheet_data.columns.intersection(website_data.columns)
combined_df = pd.merge(gsheet_data, website_data, on='sku', suffixes=('_gs', '_web'))

for column in common_cols:
    if column != 'sku':
        gsheet_col = column + '_gs'
        web_col = column + '_web'
        combined_df[f'{column}_diff'] = combined_df[gsheet_col] != combined_df[web_col]

differences_df = combined_df[combined_df[[f'{col}_diff' for col in common_cols if col != 'sku']].any(axis=1)]        
# print(differences_df)
# differences_df.to_csv("result.csv")
print(differences_df.info())
