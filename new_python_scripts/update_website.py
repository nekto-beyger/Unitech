import gspread
from google.oauth2.service_account import Credentials

# Assuming FIELD_MAP is defined somewhere in the context, mapping Hebrew fields to their English counterparts
FIELD_MAP = {
    # "Hebrew field name": "English field name",
}

def authenticate_gspread(json_keyfile_name, spreadsheet_id):
    """Authenticate with Google Sheets API and open a spreadsheet."""
    credentials = Credentials.from_service_account_file(json_keyfile_name)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(spreadsheet_id)

def extract_item_data(row, headers):
    """Extract and transform item data from a row based on predefined field mapping."""
    item_data = {}
    for hebrew_field, english_field in FIELD_MAP.items():
        field_index = headers.index(hebrew_field) if hebrew_field in headers else -1
        if field_index != -1:
            item_data[english_field] = row[field_index]
    
    # Special handling for 'visible' field
    if item_data.get("visible") == "כן":
        item_data["visible"] = True
    elif item_data.get("visible") == "לא":
        item_data["visible"] = False
    elif item_data.get("visible") == "Auto":
        item_data["visible"] = item_data.get("quantity", 0) > 0

    return item_data

def update_rows_with_differences(spreadsheet_id, json_keyfile_name):
    """Iterate through all sheets and update rows marked as different."""
    ss = authenticate_gspread(json_keyfile_name, spreadsheet_id)
    total_updated = 0

    for sheet in ss.worksheets():
        sheet_name = sheet.title
        if sheet_name not in ["SUMMARY_SHEET", "LOG_SHEET"]:  # Exclude specific sheets
            print(f"Processing sheet: {sheet_name}")
            data = sheet.get_all_values()
            headers = data[0]
            id_index = headers.index("UID")
            diff_index = headers.index("isDifferent")
            sheet_updated_count = 0

            for i, row in enumerate(data[1:], start=2):  # Skip header row
                id_ = str(row[id_index])
                is_different = row[diff_index]

                if is_different == "YES" and 3 < len(id_) < 12:
                    item_data = extract_item_data(row, headers)
                    # Update Konimbo store with item_data
                    # Assume update_konimbo_store function exists
                    # update_konimbo_store(item_data)
                    sheet_updated_count += 1

            total_updated += sheet_updated_count
            print(f"Updated {sheet_updated_count} rows in sheet: {sheet_name}")

    print(f"Total rows updated across all sheets: {total_updated}")

# Example usage
spreadsheet_id = 'your_spreadsheet_id'
json_keyfile_name = 'path_to_your_service_account_file.json'
update_rows_with_differences(spreadsheet_id, json_keyfile_name)
