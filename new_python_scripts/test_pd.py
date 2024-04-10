# import pandas as pd 
import json 


fl = '/Users/nikitabeyger/Documents/projects/unitech/response.json'

with open(fl, 'r', encoding='utf-8') as file:
    data = json.load(file)


meta_keys = [
    "cost",
    "b2bking_regular_product_price_group_2424",
    "b2bking_regular_product_price_group_2425"
]

def get_meta_values(meta_data, keys):
    meta_values = {key: None for key in keys}  # Инициализируем значения None
    for meta in meta_data:
        if meta.get("key") in keys:
            meta_values[meta.get("key")] = meta.get("value")
    return meta_values

# df = pd.json_normalize(data)

# print(df["meta_data"]["cost"])

extracted_data = []
for item in data:
    meta_values = get_meta_values(item.get("meta_data", []), meta_keys)
    
    product_data = {
        "id": item.get("id"),
        "sku": item.get("sku"),
        "stock_quantity": item.get("stock_quantity"),
        "price": item.get("price"),
        "catalog_visibility": item.get("catalog_visibility"),
        "name": item.get("name"),
        "short_description": item.get("short_description"),
        **meta_values  # Добавляем извлеченные значения meta_data
    }
    
    extracted_data.append(product_data)

# Выводим результат
for product in extracted_data:
    print(product)