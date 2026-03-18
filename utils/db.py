import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    print("Connecting with:", DB_CONFIG)
    conn = mysql.connector.connect(**DB_CONFIG)
    print("Connected successfully")
    return conn