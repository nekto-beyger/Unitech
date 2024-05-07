
from get_data_from_gsheet import get_data_from_gsheet
from get_data_from_website import get_data_from_website, get_all_products
from connection import wcapi
import pandas as pd
from update_website import get_differences, update_website

# Request to get all products; initial check if the API is accessible.
response = wcapi.get("products")
# Check if the API request was successful
if response.status_code == 200:
    # Retrieve all products from the website
    products = get_all_products()
    # Process website data
    website_data = get_data_from_website(products)
else:
    # Print error if API call failed
    print(f"Error: {response.status_code}")
    products = []
    
gsheet_data = get_data_from_gsheet()

common_cols = gsheet_data.columns.intersection(website_data.columns)
combined_df = pd.merge(gsheet_data, website_data, on='sku', suffixes=('_gs', '_web'))

for column in common_cols:
    if column != 'sku':
        gsheet_col = column + '_gs'
        web_col = column + '_web'
        combined_df[f'{column}_diff'] = combined_df[gsheet_col] != combined_df[web_col]

differences_df = combined_df[combined_df[[f'{col}_diff' for col in common_cols if col != 'sku']].any(axis=1)]        


data_to_update = get_differences(differences_df)

if data_to_update:
    update_website(data_to_update)