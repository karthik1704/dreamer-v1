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

if not os.getenv("JWT_SECRET_KEY"):
    raise ValueError("JWT_SECRET_KEY not found")
if not os.getenv("JWT_REFRESH_SECRET_KEY"):
    raise ValueError("JWT_SECRET_KEY not found")




JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY","")