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
        return str(self.id)

    def get_name(self) -> str:
        return self.name

    def get_password(self) -> str:
        return self.password

    def get_email(self) -> str:
        return self.email

    def get_role(self) -> str:
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
        self.name = name

    def set_password(self, password: str) -> None:
        self.password = password

    def set_email(self, email: str) -> None:
        self.email = email


    def set_role(self, role: str) -> None:
        self.role = role
