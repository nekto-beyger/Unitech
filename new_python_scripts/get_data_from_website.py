from connection import wcapi
import pandas as pd
import numpy as np
from read_variables import field_map_website, field_data_types_web, meta_keys
import re
from html import unescape


def clean_html(text):
    """
    Remove HTML tags, decode HTML entities, and strip whitespace from the text.
    """
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags

    text = unescape(text)  # Decode HTML entities

    text = re.sub(r'\s+', ' ', text).strip()  # Remove extraneous whitespace

    return text


def get_all_products(per_page=100):
    """
    Retrieve all products from the WooCommerce API in pages of specified size.
    """
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
    """
    Extract values from meta_data based on specified keys.

    Args:
    meta_data (list of dict): List of dictionaries containing metadata,
                              each dict has 'key' and 'value'.
    keys (list): List of keys for which values need to be extracted.

    Returns:
    dict: Dictionary with keys and their corresponding values from meta_data.
    """
    # Initialize a dictionary to hold the values for the specified keys
    meta_values = {key: None for key in keys}
    # Loop through each item in the meta_data
    for meta in meta_data:
        # Check if the 'key' in the current item exists in the specified keys
        if meta.get("key") in keys:
            # If so, update the dictionary with the value corresponding to the key
            meta_values[meta.get("key")] = meta.get("value")
    # Return the dictionary containing the extracted values
    return meta_values


def visibility(val):

    """
    Convert catalog visibility status to a boolean.
    """
    return val == 'visible'


def get_data_from_website(products):
    """
    Extract and transform product data into a structured DataFrame.
    """
    extracted_data = []
    for item in products:
        meta_values = get_meta_values(item.get("meta_data", []), meta_keys)

        product_data = {
            "id": item.get("id"),
            "sku": item.get("sku"),
            "stock_quantity": item.get("stock_quantity"),
            "manage_stock": item.get("manage_stock"),
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

    # web_df["visible"] = web_df["visible"].apply(visibility)
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

result.to_csv('result_web.csv')
# print(len(result))
# print(result.info())

# print(result.info())
