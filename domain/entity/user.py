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
        skill_lvl (Optional[str]): User's skill level (default: None)
        sports_exp (Optional[str]): User's sports experience (default: None)
        role (str): User's role (default: 'user')
    """

    id: int
    name: str
    password: str
    email: str
    skill_lvl: Optional[str] = field(default=None)
    sports_exp: Optional[str] = field(default=None)
    role: str = field(default="user")

    # --- Getters ---
    def get_id(self) -> int:
        """Get the user ID"""
        return self.id

    def get_name(self) -> str:
        """Get the user's name"""
        return self.name

    def get_password(self) -> str:
        """Get the user's password hash"""
        return self.password

    def get_email(self) -> str:
        """Get the user's email address"""
        return self.email

    def get_skill_lvl(self) -> Optional[str]:
        """Get the user's skill level"""
        return self.skill_lvl

    def get_sports_exp(self) -> Optional[str]:
        """Get the user's sports experience"""
        return self.sports_exp

    def get_role(self) -> str:
        """Get the user's role"""
        return self.role

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

    def set_skill_lvl(self, skill_lvl: str) -> None:
        """Set the user's skill level

        Args:
            skill_lvl (str): New skill level
        """
        self.skill_lvl = skill_lvl

    def set_sports_exp(self, sports_exp: str) -> None:
        """Set the user's sports experience

        Args:
            sports_exp (str): New sports experience
        """
        self.sports_exp = sports_exp

    def set_role(self, role: str) -> None:
        """Set the user's role

        Args:
            role (str): New role
        """
        self.role = role
