from data_source.user_queries import update_user_profile_by_id, remove_user_profile_picture

class ProfileManagement:
    def updateProfile(self, user_id, name, password, profile_picture=None):
        if profile_picture is None:
            profile_picture = ""
        return update_user_profile_by_id(user_id, name, password, profile_picture)

    def removeProfilePicture(self, user_id):
        return remove_user_profile_picture(user_id) 