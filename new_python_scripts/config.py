
from dotenv import load_dotenv
import os

load_dotenv()  # Загружает переменные окружения из файла .env

path_to_cred = os.getenv('GOOGLE_CREDENTIALS_PATH')
# print(path_to_cred)