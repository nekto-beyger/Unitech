import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials
from update_sheet import update_sheet_with_item_details

# Function to authenticate with Google Sheets and access a spreadsheet
# def authenticate_gspread(json_keyfile_name, spreadsheet_id):
#     # Using OAuth2 credentials to authorize and create a client.
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, 
#                                                                     ['https://spreadsheets.google.com/feeds',
#                                                                      'https://www.googleapis.com/auth/drive'])
#     gc = gspread.authorize(credentials)
#     # Opening the spreadsheet by its ID.
#     return gc.open_by_key(spreadsheet_id)

# Function for randomly selecting and processing a third of the sheets
def run_get_on_random_third_sheets(spreadsheet_id, json_keyfile_name, exclude_sheets):
    # Authenticate and get the spreadsheet object
    sh = authenticate_gspread(json_keyfile_name, spreadsheet_id)
    # Getting all sheets in the spreadsheet
    all_sheets = sh.worksheets()
    # Getting a random third of the sheets
    sheets_to_process = get_random_third(all_sheets)
    
    # Processing each selected sheet
    for sheet in sheets_to_process:
        sheet_name = sheet.title
        print(f'Begins Sheet: {sheet_name}')
        # If the sheet name is not in the exclude list, update it.
        if sheet_name not in exclude_sheets:
            # Call your update function here
            # updateSheetWithItemDetails(sheet)
            update_sheet_with_item_details(sheet_name)
        print(f'Done Sheet: {sheet_name}')

# Function to get a random third of the sheets
def get_random_third(sheets):
    total_sheets = len(sheets)
    number_of_sheets_to_process = round(total_sheets / 3)
    # Randomly selecting sheets
    selected_sheets = random.sample(sheets, number_of_sheets_to_process)
    
    # Logging the names of selected sheets
    selected_sheet_names = [sheet.title for sheet in selected_sheets]
    print(f"Selected Sheets: {', '.join(selected_sheet_names)}")
    
    return selected_sheets

# Example usage
SPREADSHEET_ID = 'your_spreadsheet_id_here'  # Replace with your actual spreadsheet ID
JSON_KEYFILE_NAME = 'path_to_your_service_account_json_keyfile.json'  # Replace with the path to your JSON key file
EXCLUDE_SHEETS = ['Log', 'KonimboSheet']  # Sheets to exclude from processing

# Running the function with the given parameters
run_get_on_random_third_sheets(SPREADSHEET_ID, JSON_KEYFILE_NAME, EXCLUDE_SHEETS)
