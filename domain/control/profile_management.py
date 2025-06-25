from data_source.user_queries import update_user_profile

class ProfileManagement:
    def updateProfile(self, user_id, name, password, email, skill_lvl=None, sports_exp=None):
        return update_user_profile(user_id, name, password, email, skill_lvl, sports_exp) 