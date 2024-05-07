from get_data_from_gsheet import get_data_from_gsheet
from get_data_from_website import get_data_from_website, get_all_products
from update_website import get_differences, update_website
from connection import wcapi
import re 
import pandas as pd


def filter_products_by_sku_pattern(products, pattern):
    pattern = re.compile(pattern)
    return [product for product in products if pattern.search(product['sku'])]


gdata = get_data_from_gsheet()

response = wcapi.get("products")

if response.status_code == 200:
    products = get_all_products()
    filtered_products = filter_products_by_sku_pattern(products, '4998')
    result = get_data_from_website(filtered_products)
else:
    print(f"Error: {response.status_code}")
    products = []

# filtered_products_df = pd.DataFrame(filtered_products) 

# print(result.info())

# for product in result.itertuples():
#     print(product.sku, product.name)

common_cols = gdata.columns.intersection(result.columns)
combined_df = pd.merge(gdata, result, on='sku', suffixes=('_gs', '_web'))

# print(combined_df.info())

for column in common_cols:
    if column != 'sku':
        gsheet_col = column + '_gs'
        web_col = column + '_web'
        combined_df[f'{column}_diff'] = combined_df[gsheet_col] != combined_df[web_col]

differences_df = combined_df[combined_df[[f'{col}_diff' for col in common_cols if col != 'sku']].any(axis=1)]        

cols_to_drop = ['id_gs', 'sale_price', 'cost_gs', 'cost_web', 'cost_', 'cost_diff', 'id_diff']
cols_to_drop = [col for col in cols_to_drop if col in differences_df.columns]
differences_df.drop(cols_to_drop, axis=1, inplace=True)

# differences_df.rename(columns={"visibility": "visible_web"}, inplace=True)

# print(differences_df.info())
# differences_df.to_csv('result.csv')
# print(differences_df)
data_to_update = get_differences(differences_df)
# print('+++++++++++++++')
# print(data_to_update)

if data_to_update:
    update_website(data_to_update)