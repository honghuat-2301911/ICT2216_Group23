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
        INSERT INTO user (name, password, email, role)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (
            user_data["name"],
            user_data["password"],
            user_data["email"],
            user_data.get("role", "user"),
        ),
    )
    connection.commit()
    cursor.close()
    connection.close()
    return True


def get_user_by_id(user_id: int):
    """
    Retrieve user data by user ID

    Args:
        user_id (int): The ID of the user

    Returns:
        dict or None: User data dictionary if found, else None
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_data


def update_user_profile_by_id(user_id: int, name: str, password: str) -> bool:
    """
    Update a user's profile by user ID.

    Args:
        user_id (int): The ID of the user to update.
        name (str): The new name for the user.
        password (str): The new password for the user.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "UPDATE user SET name = %s, password = %s WHERE id = %s"
        cursor.execute(query, (name, password, user_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Update failed:", e)
        return False
    finally:
        cursor.close()
        connection.close()


def search_users_by_name(search_term: str, limit: int = 10):
    """
    Search for users by name with partial matching

    Args:
        search_term (str): The search term to match against user names
        limit (int): Maximum number of results to return

    Returns:
        list: List of user dictionaries matching the search term
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT id, name, email 
            FROM user 
            WHERE name LIKE %s 
            ORDER BY name 
            LIMIT %s
        """
        search_pattern = f"%{search_term}%"
        cursor.execute(query, (search_pattern, limit))
        users = cursor.fetchall()
        return users
    except Exception as e:
        print(f"Search failed: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
