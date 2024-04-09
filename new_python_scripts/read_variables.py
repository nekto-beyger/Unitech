import json 
import os 

current_dir = os.path.dirname(os.path.abspath(__file__))

json_path = os.path.join(current_dir, 'variables.json')

with open(json_path, 'r') as file:
    data = json.load(file)
    
    
your_token = data["YOUR_TOKEN"]

api_endpoint = data["API_ENDPOINT"]

field_map = data["FIELD_MAP"]

relevant_fields = data["RELEVANT_FIELDS"]

gsheet_id = data["GSHEET_ID"]

columns = data["COLUMNS"]

field_data_types = data["FILED_DATA_TYPES"]

# print(gsheet_id)