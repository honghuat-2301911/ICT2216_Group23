"""User login management for authentication and session handling"""

from flask import g
from flask_login import login_user as flask_login_user, logout_user as flask_logout_user
import bcrypt

from data_source.user_queries import get_user_by_email
from domain.entity.user import User


def login_user(email: str, password: str):
    """
    Attempt to authenticate a user by email and password

    Args:
        email (str): User's email address
        password (str): User's password

    Returns:
        User: The authenticated User object if found, else None
    """
    result = get_user_by_email(email)
    if not result:
        return None

    # Check password hash
    stored_hash = result["password"]
    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return None

    user = User(
        id=result["id"],
        name=result["name"],
        password=result["password"],
        email=result["email"],
        role=result.get("role", "user"),
    )

    flask_login_user(user)
    return user


def logout_user():
    """Log out the current user using flask_login"""
    flask_logout_user()


def get_user_display_data():
    """
    Retrieve display data for the currently logged-in user

    Returns:
        dict: User display information, or None if no user is logged in
    """
    user = g.get("current_user")
    if not user:
        return None

    return {
        # "id": user.get_id(),  # Uncomment if you want to display user ID
        "name": user.get_name(),
        "email": user.get_email(),
        "role": user.get_role(),
    }