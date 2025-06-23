from domain.entity.user import User
from data_source.user_queries import *;

from dataclasses import asdict

def register_user(user_data: dict) -> bool:
    """
    Register a new user in the system.
    :param user_data: A dictionary containing user information.
    :return: True if registration is successful, False otherwise.
    """
    existing_user = get_user_by_email(user_data['email'])
    if existing_user:
        print("User already exists with this email.")
        return False

    # # Create a User entity (includes manually set `id`)
    # user = User(**user_data)

    # Insert the new user into the database using asdict()
    return insert_user(user_data)
