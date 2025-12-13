import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    try:
        conn=mysql.connector.connect(
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Помилка{err}")

    