from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = True

db_config = {
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'db_name': os.getenv('DB_NAME')
}