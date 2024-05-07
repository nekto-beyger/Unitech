from connection import wcapi
from read_variables import field_map_website


def get_key_by_value(target_value, dictionary):
    """
    Return the key corresponding to the given value in the dictionary.
    """
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None


def update_website(updates):
    """
    Send update requests to the WooCommerce API for each product in the updates list.

    Args:
    updates (list): List of dictionaries containing product IDs and their updates.
    """
    for update in updates:
        product_id = update['id']
        data = update['updates']
        response = wcapi.put(f"products/{product_id}", data)
        if response.status_code == 200:
            print(f"Product {product_id} updated successfully.")
        else:
            print(f"Failed to update product {product_id}. Status code: {response.status_code}")


def get_differences(diff_df):
    """
    Generate update data for products that need synchronization between Google Sheets and the website.

    Args:
    diff_df (DataFrame): DataFrame with products that have differences marked with a '_diff' suffix.

    Returns:
    list: List of dictionaries where each dictionary contains the product ID and the updates needed.
    """
    updates = []
    for key, row in diff_df.iterrows():
        update_needed = False
        upd_data = {"id": row['id_web'], "updates": {}}
        api_fields = ['quantity', 'price_1', 'price_2', 'price_3', 'price']

        for api_field in api_fields:
            # print(f"{api_field}_diff")
            # print(row.get(f"{api_field}_diff"))
            if row.get(f"{api_field}_diff"):
                local_field = get_key_by_value(api_field, field_map_website)  # Get the local field name from API field
                # print(local_field)
                upd_data['updates'][local_field] = row.get(f"{api_field}_gs")
                # print(upd_data)
                update_needed = True

        if update_needed:
            updates.append(upd_data)

    return updates
