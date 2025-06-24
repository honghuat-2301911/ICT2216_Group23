"""Authentication management for password hashing and verification"""

import bcrypt


def hash_password(plain_text_password: str) -> str:
    """
    Hash plaintext password using bcrypt

    Args:
        plain_text_password (str): The plaintext password

    Returns:
        str: Hashed password as a UTF-8 string
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password (result is in bytes)
    hashed = bcrypt.hashpw(plain_text_password.encode("utf-8"), salt)
    # Return as a decoded string for storage (e.g. in MySQL)
    return hashed.decode("utf-8")


def check_password(plain_text_password: str, hashed_password: str) -> bool:
    """
    Check if a plaintext password matches the given bcrypt hash

    Args:
        plain_text_password (str): The plaintext password
        hashed_password (str): The hashed password as stored

    Returns:
        bool: True if the password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_text_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
