import requests
import json
import gspread
from google.oauth2.service_account import Credentials

# Assuming these global variables are defined somewhere in the context
SUMMARY_SHEET = 'Summary'
YOUR_TOKEN = 'your_konimbo_api_token'
API_ENDPOINT = 'https://api.konimbo.co.il/v1/items/'

# Authenticate and get the spreadsheet
def authenticate_gspread(json_keyfile_name, spreadsheet_id):
    credentials = Credentials.from_service_account_file(json_keyfile_name, scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ])
    gc = gspread.authorize(credentials)
    return gc.open_by_key(spreadsheet_id)

def update_konimbo_store(item_data, spreadsheet_id, json_keyfile_name):
    ss = authenticate_gspread(json_keyfile_name, spreadsheet_id)
    sheet = ss.worksheet(SUMMARY_SHEET)
    
    print("itemData:", item_data)
    
    # Constructing the discount_prices part of the payload
    discount_prices = {
        "field_18653": item_data["discount_prices"]["field_18653"],
        "field_18682": item_data["discount_prices"]["field_18682"],
        "field_19032": item_data["discount_prices"]["field_19032"]
    }
    print("discount_prices:", discount_prices)
    
    # Construct the full payload
    payload = {
        "token": YOUR_TOKEN,
        "item": {
            "id": item_data["id"],
            "quantity": item_data["quantity"],
            "cost": item_data["cost"],
            "price": item_data["price"],
            "visible": item_data["visible"],
            "desc": item_data["desc"],
            "discount_prices": discount_prices,
            "inventory": [
                {
                    "code": "",
                    "free": item_data["quantity"]  # Assuming "free" matches "quantity"
                }
            ]
        }
    }
    
    # Prepare the request options
    headers = {
        'Authorization': f'Bearer {YOUR_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Make the API call
        response = requests.put(API_ENDPOINT + str(item_data["id"]), headers=headers, json=payload)
        status_code = response.status_code
        content = response.text
        
        if status_code == 200:
            print(f"API call returned statusCode: {status_code}")
        else:
            print(f"API call returned statusCode: {status_code}")
        
        return {"success": True, "statusCode": status_code, "content": content}
    except Exception as e:
        print(f"Error updating Konimbo: {str(e)}")
        return {"success": False, "statusCode": 0, "content": ''}

# Example usage
# Define your `item_data` structure as per your requirements
item_data = {
    "id": "example_id",
    "quantity": 10,
    "cost": 100,
    "price": 150,
    "visible": True,
    "desc": "Example description",
    "discount_prices": {"field_18653": 120, "field_18682": 110, "field_19032": 100}
}

spreadsheet_id = 'your_spreadsheet_id'
json_keyfile_name = 'path_to_your_service_account_file.json'

result = update_konimbo_store(item_data, spreadsheet_id, json_keyfile_name)
print(result)
