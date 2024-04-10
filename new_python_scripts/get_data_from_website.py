from connection import wcapi

response = wcapi.get("products?sku=4952-1")
print(response.status_code)
print(response.json())
# import requests
# from requests.auth import HTTPBasicAuth

# url = "https://www.usys.co.il/wp-json/wc/v3"
# consumer_key = "consumer_key"
# consumer_secret = "consumer_secret"

# response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

# # Проверяем статус ответа
# if response.status_code == 200:
#     # Выводим JSON ответа
#     print(response.json())
# else:
#     print(f"Error: {response.status_code}")