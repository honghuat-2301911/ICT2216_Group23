from data_source.user_queries import update_user_profile_by_id

class ProfileManagement:
    def updateProfile(self, user_id, name, password):
        return update_user_profile_by_id(user_id, name, password) 