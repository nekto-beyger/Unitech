import gspread
from google.oauth2.service_account import Credentials

# Load your credentials and open the spreadsheet
credentials = Credentials.from_service_account_file('path_to_your_service_account_file.json')
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key('your_spreadsheet_id')

# Define your field map and sheets to exclude
FIELD_MAP = {
    "UID": "id",
    "זמינות": "quantity",
    # Add other mappings here
}
EXCLUDE_SHEETS = ["Log", "KonimboSheet"]

def detect_changes_in_all_sheets():
    sheets = spreadsheet.worksheets()
    total_differences = 0
    
    for sheet in sheets:
        sheet_name = sheet.title
        if sheet_name not in EXCLUDE_SHEETS:
            print(f"Processing sheet: {sheet_name}")
            differences = check_differences(sheet)
            total_differences += differences
            print(f"Sheet: {sheet_name}, Differences detected: {differences}")
    
    print(f"Total differences detected in all sheets: {total_differences}")

def check_differences(sheet):
    data = sheet.get_all_values()
    headers = data[0]
    differences_count = 0
    
    # Determine the column index for 'isDifferent'
    output_column_index = headers.index("isDifferent") if "isDifferent" in headers else len(headers)
    
    # Add 'isDifferent' column if it doesn't exist
    if output_column_index == len(headers):
        sheet.update_cell(1, output_column_index + 1, "isDifferent")
    
    # Iterate through each row to find differences
    for i, row in enumerate(data[1:], start=2):  # Skipping headers, gspread is 1-indexed
        is_different = ""
        for field, mapped_field in FIELD_MAP.items():
            if field in headers and mapped_field in headers:
                left_index = headers.index(field) + 1  # Adjusting index for gspread
                right_index = headers.index(mapped_field) + 1
                left_value = row[left_index - 1]  # Correcting index for zero-based lists
                right_value = row[right_index - 1]
                
                # Example check (you'll need to implement your logic based on FIELD_MAP)
                if left_value != right_value:
                    is_different = "YES"
                    break  # Found a difference, no need to check further fields
        
        # Update the 'isDifferent' column for the row
        sheet.update_cell(i, output_column_index + 1, is_different)
        if is_different == "YES":
            differences_count += 1

    return differences_count

# Example usage
detect_changes_in_all_sheets()
