from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """
    User entity that mirrors the `user` table in MySQL.
    Compatible with `User(**row)` where row is a dict from SQL query.
    """
    id: int
    name: str
    password: str  # Hash in production
    email: str
    skill_lvl: Optional[str] = None
    sports_exp: Optional[str] = None
    role: str = "user"


    # ---------------- Getters ----------------
    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_password(self) -> str:
        return self.password

    def get_email(self) -> str:
        return self.email

    def get_skill_lvl(self) -> Optional[str]:
        return self.skill_lvl

    def get_sports_exp(self) -> Optional[str]:
        return self.sports_exp

    def get_role(self) -> str:
        return self.role

    # ---------------- Setters ----------------
    def set_name(self, name: str) -> None:
        self.name = name

    def set_password(self, password: str) -> None:
        self.password = password

    def set_email(self, email: str) -> None:
        self.email = email

    def set_skill_lvl(self, skill_lvl: Optional[str]) -> None:
        self.skill_lvl = skill_lvl

    def set_sports_exp(self, sports_exp: Optional[str]) -> None:
        self.sports_exp = sports_exp

    def set_role(self, role: str) -> None:
        self.role = role
