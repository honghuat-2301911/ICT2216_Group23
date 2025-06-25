from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    id: int
    name: str
    password: str
    email: str
    skill_lvl: Optional[str] = field(default=None)
    sports_exp: Optional[str] = field(default=None)
    role: str = field(default="user")

    # --- Getters ---
    def get_id(self): return self.id
    def get_name(self): return self.name
    def get_password(self): return self.password
    def get_email(self): return self.email
    def get_skill_lvl(self): return self.skill_lvl
    def get_sports_exp(self): return self.sports_exp
    def get_role(self): return self.role

    # --- Setters ---
    def set_name(self, name: str): self.name = name
    def set_password(self, password: str): self.password = password
    def set_email(self, email: str): self.email = email
    def set_skill_lvl(self, skill_lvl: str): self.skill_lvl = skill_lvl
    def set_sports_exp(self, sports_exp: str): self.sports_exp = sports_exp
    def set_role(self, role: str): self.role = role
