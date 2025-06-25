"""Database for MySQL"""

import os

import mysql.connector
from mysql.connector import Error


def get_connection():
    """
    Establish and return a MySQL database connection using env variables

    Return:
        The database connection if successful, otherwise None
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", ""),
        )
        if connection.is_connected():
            return connection
        return None  # Return None if not connected
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None
