import gspread
import pandas as pd
from read_variables import your_token, api_endpoint, gsheet_id
from api_getter import get_multiple_konimbo_item_details
from config import path_to_cred


def update_sheet_with_item_details(sheet_name):
    # Authentication and sheet retrieval
    gc = gspread.service_account(filename=path_to_cred)
    sh = gc.open(gsheet_id)  # The name of your Google Sheets document
    sheet = sh.worksheet(sheet_name)
    
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
        return
    
    # Fetching item details using the external function
    item_details = get_multiple_konimbo_item_details(item_ids, your_token)
    if not item_details:
        print("No item details fetched.")
        return
    
    # Writing headers to the spreadsheet
    headers_range = f"AB1:AB{len(RELEVANT_FIELDS)}"  # Assuming data should start from the 28th column (AB)
    sheet.update(headers_range, [RELEVANT_FIELDS], value_input_option='RAW')
    
    # Writing item details to the spreadsheet
    for details in item_details:
        row = item_ids_to_rows_map.get(str(details['id']))
        if row:
            data_range = f"AB{row}:AB{row+len(RELEVANT_FIELDS)-1}"
            sheet.update(data_range, [[details[field] for field in RELEVANT_FIELDS]], value_input_option='RAW')

# Example usage
SHEET_NAME = 'Sheet1'  # Make sure to use the actual name of your sheet
update_sheet_with_item_details(SHEET_NAME)
