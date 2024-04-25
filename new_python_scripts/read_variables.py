import json 
import os 
import pandas as pd
current_dir = os.path.dirname(os.path.abspath(__file__))

json_path = os.path.join(current_dir, 'variables.json')


def convert_dtype(dtype_str):
    if dtype_str.startswith('Int'):
        return pd.Int64Dtype() if dtype_str == 'Int64' else pd.Int32Dtype() if dtype_str == 'Int32' else pd.Int8Dtype()
    elif dtype_str == 'bool':
        return pd.BooleanDtype()
    elif dtype_str.startswith('float'):
        return 'float64'
    return dtype_str


with open(json_path, 'r') as file:
    data = json.load(file)
    field_data_types = {k: convert_dtype(v) for k, v in data["FILED_DATA_TYPES"].items()}
    field_data_types_web = {k: convert_dtype(v) for k, v in data["FILED_DATA_TYPES_WEB"].items()}
    
your_token = data["YOUR_TOKEN"]

api_endpoint = data["API_ENDPOINT"]

field_map_gsheet = data["FIELD_MAP_GSHEET"]

field_map_website = data["FIELD_MAP_WEBSITE"]

relevant_fields = data["RELEVANT_FIELDS"]

gsheet_id = data["GSHEET_ID"]

columns = data["COLUMNS"]

