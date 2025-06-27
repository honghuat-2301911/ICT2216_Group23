"""Define user entity for the application"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    """A user class

    Attributes:
        id (int): Unique ID for the user
        name (str): User's name
        password (str): User's password hash
        email (str): User's email address
        role (str): User's role (default: 'user')
    """

    id: int
    name: str
    password: str
    email: str
    role: str = field(default="user")

    # --- Getters ---
    def get_id(self):
        """Return the user ID as a string for Flask-Login compatibility"""
        return str(self.id)

    def get_name(self) -> str:
        """Get the user's name"""
        return self.name

    def get_password(self) -> str:
        """Get the user's password hash"""
        return self.password

    def get_email(self) -> str:
        """Get the user's email address"""
        return self.email

    def get_role(self) -> str:
        """Get the user's role"""
        return self.role

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # --- Setters ---
    def set_name(self, name: str) -> None:
        """Set the user's name

        Args:
            name (str): New display name
        """
        self.name = name

    def set_password(self, password: str) -> None:
        """Set the user's password

        Args:
            password (str): New password hash
        """
        self.password = password

    def set_email(self, email: str) -> None:
        """Set the user's email address

        Args:
            email (str): New email address
        """
        self.email = email


    def set_role(self, role: str) -> None:
        """Set the user's role

        Args:
            role (str): New role
        """
        self.role = role
