class User:
    def __init__(self, id, name, password, email, skill_lvl=None, sports_exp=None, role="user"):
        self._id = id
        self._name = name
        self._password = password
        self._email = email
        self._skill_lvl = skill_lvl
        self._sports_exp = sports_exp
        self._role = role

    # Getters
    def get_id(self): return self._id
    def get_name(self): return self._name
    def get_password(self): return self._password
    def get_email(self): return self._email
    def get_skill_lvl(self): return self._skill_lvl
    def get_sports_exp(self): return self._sports_exp
    def get_role(self): return self._role

    # Setters
    def set_name(self, name): self._name = name
    def set_password(self, password): self._password = password
    def set_email(self, email): self._email = email
    def set_skill_lvl(self, skill_lvl): self._skill_lvl = skill_lvl
    def set_sports_exp(self, sports_exp): self._sports_exp = sports_exp
    def set_role(self, role): self._role = role
