from connection import gc
from read_variables import your_token, api_endpoint, gsheet_id

sh = gc.open(gsheet_id)  # The name of your Google Sheets document
for sheet in sh:

# Retrieving values from column B
    column_b_values = sheet.col_values(2)  # gspread indexes columns and rows starting from 1
    item_ids_to_rows_map = {}
    for index, value in enumerate(column_b_values, start=1):
        value = value.strip()
        if len(value) >= 5 and value.isdigit():
            item_ids_to_rows_map[value] = index

    item_ids = list(item_ids_to_rows_map.keys())
    if not item_ids:
        print("No valid item IDs found in column B.")
    
print(item_ids)