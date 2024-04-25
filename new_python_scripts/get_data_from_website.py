from connection import wcapi
import pandas as pd
import numpy as np
from read_variables import field_map_website
from read_variables import field_data_types_web
import re
from html import unescape

def clean_html(text):
    text = re.sub(r'<.*?>', '', text)
    # Декодирование HTML-сущностей
    text = unescape(text)
    # Удаление непечатаемых символов
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_all_products(per_page=100):
    page = 1
    all_products = []
    while True:
        response = wcapi.get(f"products?per_page={per_page}&page={page}")
        products = response.json()
        if not products:
            break
        all_products.extend(products)
        page += 1
    return all_products


def get_meta_values(meta_data, keys):
    meta_values = {key: None for key in keys}
    for meta in meta_data:
        if meta.get("key") in keys:
            meta_values[meta.get("key")] = meta.get("value")
    return meta_values


def visibility(val):
    if val == 'visible':
        return True
    else:
        return False

def get_data_from_website(products):

    meta_keys = [
        "cost",
        "b2bking_regular_product_price_group_2424",
        "b2bking_regular_product_price_group_2425",
        "b2bking_regular_product_price_group_2426",
        "acf-field_65fc592a937b9"
    ]

    extracted_data = []
    for item in products:
        meta_values = get_meta_values(item.get("meta_data", []), meta_keys)

        product_data = {
            "id": item.get("id"),
            "sku": item.get("sku"),
            "stock_quantity": item.get("stock_quantity"),
            "price": item.get("regular_price"),
            "sale_price": item.get("sale_price"),
            "catalog_visibility": item.get("catalog_visibility"),
            "name": item.get("name"),
            "short_description": item.get("short_description"),
            **meta_values
        }

        extracted_data.append(product_data)

    web_df = pd.DataFrame(extracted_data)

    web_df = web_df[list(field_map_website.keys())]
    web_df.columns = list(field_map_website.values())
    
    web_df["visible"] = web_df["visible"].apply(visibility)
    web_df["desc"] = web_df["desc"].apply(clean_html)
    web_df["desc"] = web_df["desc"].str.replace('″', '"')

    web_df = web_df.replace('', np.nan).infer_objects()
    web_df = web_df.fillna(value=np.nan)
    web_df = web_df.astype(field_data_types_web)

    return web_df


response = wcapi.get("products")

if response.status_code == 200:
    products = get_all_products()
    result = get_data_from_website(products)
else:
    print(f"Error: {response.status_code}")
    products = []

# result = result.query("b2bking_regular_product_price_group_2424 != price_1 or b2bking_regular_product_price_group_2425 != price_2 or b2bking_regular_product_price_group_2426 != price_3")

# result.to_csv('result.csv')
# print(len(result))
# print(result.info())

# print(result.info())
