"""Database queries for user operations"""

import mysql.connector

from data_source.db_connection import get_connection


def get_user_by_email(email: str):
    """
    Retrieve user data by email

    Args:
        email (str): The email address of the user

    Returns:
        dict or None: User data dictionary if found, else None
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_data


# def insert_user(user_data: dict) -> bool:
#     """
#     Insert a new user into the database

#     Args:
#         user_data (dict): Dictionary containing user information

#     Returns:
#         bool: True if insertion is successful, False otherwise
#     """
#     try:
#         connection = get_connection()
#         cursor = connection.cursor()
#         query = """
#             INSERT INTO user (name, password, email, skill_lvl, sports_exp, role)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(
#             query,
#             (
#                 user_data["name"],
#                 user_data["password"],
#                 user_data["email"],
#                 user_data.get("skill_lvl"),
#                 user_data.get("sports_exp"),
#                 user_data.get("role", "user"),
#             ),
#         )
#         connection.commit()
#         return True
#     except mysql.connector.Error as e:
#         print("Insert failed:", e)
#         return False
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()

def insert_user(user_data: dict) -> bool:
    """
    Insert a new user into the database

    Args:
        user_data (dict): Dictionary containing user information

    Returns:
        bool: True if insertion is successful, False otherwise
    """
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO user (name, password, email, skill_lvl, sports_exp, role)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (
            user_data["name"],
            user_data["password"],
            user_data["email"],
            user_data.get("skill_lvl"),
            user_data.get("sports_exp"),
            user_data.get("role", "user"),
        ),
    )
    connection.commit()
    cursor.close()
    connection.close()
    return True
