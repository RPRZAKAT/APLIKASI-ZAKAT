import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            port=int(os.environ["DB_PORT"]),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
            ssl_ca="ca.pem"
        )
        return conn

    except Error as e:
        print(f"Gagal koneksi database: {e}")
        raise