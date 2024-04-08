import requests
import time
import pandas as pd
from read_variables import your_token, api_endpoint


def get_multiple_konimbo_item_details(item_ids, token):
    api_endpoint = api_endpoint
    attributes = [
        "id", "quantity", "cost", "price", "visible", "title", "desc", "discount_prices"
    ]
    
    # Preparing the list to store product data
    items_data = []
    
    for item_id in item_ids:
        attributes_query = ','.join(attributes)
        url = f"{api_endpoint}{item_id}?token={token}&attributes={attributes_query}"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                item_data = response.json()
                
                # Assuming discount_prices is a dictionary and adding it separately
                item_data_flat = {
                    "id": item_data.get("id"),
                    "quantity": item_data.get("quantity"),
                    "cost": item_data.get("cost"),
                    "price": item_data.get("price"),
                    "visible": item_data.get("visible"),
                    "title": item_data.get("title"),
                    "desc": item_data.get("desc"),
                    **item_data.get("discount_prices", {})
                }
                
                items_data.append(item_data_flat)
            else:
                print(f"Failed to fetch item details for item ID {item_id}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching item details for item ID {item_id}: {str(e)}")
        
        # Wait before the next API request
        time.sleep(1)
    
    # Converting the list of dictionaries into a DataFrame
    items_df = pd.DataFrame(items_data)
    
    return items_df




# Example usage
item_ids = ['123', '456']  # Example item IDs
token = your_token
results_df = get_multiple_konimbo_item_details(item_ids, token)
print(results_df)
