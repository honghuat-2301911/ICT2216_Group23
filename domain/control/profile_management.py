from data_source.bulletin_queries import (
    get_joined_user_names_by_activity_id,
    get_all_bulletin,
    get_sports_activity_by_id,
    update_sports_activity,
    update_sports_activity_details,
)
from data_source.user_queries import (
    remove_user_profile_picture,
    update_user_profile_by_id,
    get_user_by_id,
)

from data_source.social_feed_queries import get_posts_by_user_id
from domain.entity.user import User
from domain.entity.sports_activity import SportsActivity
import os
import uuid
import bcrypt
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename
from domain.control.otp_management import generate_otp_for_user, verify_and_enable_otp
from domain.control.social_feed_management import deletePost, editPost

class ProfileManagement:
    def updateProfile(self, user_id, name, password, profile_picture=None):
        if profile_picture is not None:
            return update_user_profile_by_id(user_id, name, password, profile_picture)
        else:
            return update_user_profile_by_id(user_id, name, password)

    def removeProfilePicture(self, user_id):
        return remove_user_profile_picture(user_id)

    def get_joined_user_names(self, activity_id):
        return get_joined_user_names_by_activity_id(activity_id)

    def get_user_profile(self, user_id):
        user_data = get_user_by_id(user_id)
        if not isinstance(user_data, dict):
            return None
        id_val = user_data.get("id")
        if isinstance(id_val, int):
            user_id_val = id_val
        elif isinstance(id_val, str) and id_val.isdigit():
            user_id_val = int(id_val)
        else:
            user_id_val = 0
        return User(
            user_id_val,
            str(user_data.get("name")) if user_data.get("name") is not None else "",
            (
                str(user_data.get("password"))
                if user_data.get("password") is not None
                else ""
            ),
            str(user_data.get("email")) if user_data.get("email") is not None else "",
            str(user_data.get("role", "user")),
            str(user_data.get("profile_picture", "")),
            user_data.get("otp_secret"),
            bool(int(user_data.get("otp_enabled", 0))),
        )

    def get_user_posts(self, user_id):
        return get_posts_by_user_id(user_id)

    def get_user_activities(self, user_id):
        all_activities = get_all_bulletin()
        hosted_activities = []
        joined_only_activities = []
        def get_val(r, key, default=None):
            if isinstance(r, dict):
                return r.get(key, default)
            return getattr(r, key, default)
        def safe_int(val, default=0):
            try:
                return int(val)
            except (TypeError, ValueError):
                return default
        if all_activities:
            for row in all_activities:
                activity = SportsActivity(
                    id=safe_int(get_val(row, 'id', 0)),
                    user_id=safe_int(get_val(row, 'user_id', 0)),
                    activity_name=str(get_val(row, 'activity_name', '')),
                    activity_type=str(get_val(row, 'activity_type', '')),
                    skills_req=str(get_val(row, 'skills_req', '')),
                    date=str(get_val(row, 'date', '')),
                    location=str(get_val(row, 'location', '')),
                    max_pax=safe_int(get_val(row, 'max_pax', 0)),
                    user_id_list_join=str(get_val(row, 'user_id_list_join', '')),
                )
                if activity.user_id == user_id:
                    hosted_activities.append(activity)
                else:
                    joined_ids = [
                        uid.strip()
                        for uid in (activity.user_id_list_join or '').split(',')
                        if uid.strip()
                    ]
                    if str(user_id) in joined_ids:
                        joined_only_activities.append(activity)
        return hosted_activities, joined_only_activities

    def update_profile_full(self, user_id, form):
        name = form.name.data
        password = form.password.data
        profile_picture_url = None
        remove_picture = form.remove_profile_picture.data

        # Handle file upload
        if form.profile_picture.data:
            file = form.profile_picture.data
            try:
                file.seek(0)
                image = Image.open(file)
                image.verify()  # Raises if not a valid image
                file.seek(0)    # Reset pointer for saving
            except (UnidentifiedImageError, Exception):
                flash("Uploaded profile picture is not a valid image.", "error")
                return False

            ext = os.path.splitext(secure_filename(file.filename))[1]
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            image_path = os.path.join(
                "presentation", "static", "images", "profile", unique_filename
            )
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            file.save(image_path)
            profile_picture_url = f"/static/images/profile/{unique_filename}"
        elif remove_picture:
            profile_picture_url = ""
        # Password logic
        if password:
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            if profile_picture_url is not None:
                result = self.updateProfile(
                    user_id, name, hashed_password, profile_picture_url
                )
            else:
                result = self.updateProfile(user_id, name, hashed_password)
        else:
            user_data = get_user_by_id(user_id)
            current_password = (
                user_data["password"]
                if isinstance(user_data, dict) and "password" in user_data
                else ""
            )
            if profile_picture_url is not None:
                result = self.updateProfile(
                    user_id, name, current_password, profile_picture_url
                )
            else:
                result = self.updateProfile(user_id, name, current_password)
        return result

    def edit_activity(self, user_id, activity_id, form):
        activity = get_sports_activity_by_id(activity_id)
        def get_val(r, key, default=None):
            if isinstance(r, dict):
                return r.get(key, default)
            return getattr(r, key, default)
        def safe_int(val, default=0):
            try:
                return int(val)
            except (TypeError, ValueError):
                return default
        if not activity or safe_int(get_val(activity, 'user_id', 0)) != user_id:
            return False, "You are not authorized to edit this activity."
        if form.validate_on_submit():
            update_sports_activity_details(
                activity_id,
                form.activity_name.data,
                form.activity_type.data,
                form.skills_req.data,
                form.date.data.strftime("%Y-%m-%d %H:%M:%S") if form.date.data else "",
                form.location.data,
                form.max_pax.data,
                get_val(activity, 'user_id_list_join', ""),
            )
            return True, "Activity updated successfully."
        return False, "Failed to update activity. Check the fields."

    def edit_post(self, user_id, post_id, form):
        if form.validate_on_submit():
            updated_content = form.content.data or ""
            remove_image = form.remove_image.data
            success = editPost(user_id, post_id, updated_content, remove_image)
            if success:
                return True, "Post updated successfully."
            else:
                return False, "Failed to update post."
        return False, "Failed to update post. Please check the fields."

    def leave_activity(self, user_id, activity_id):
        activity = get_sports_activity_by_id(activity_id)
        def get_val(r, key, default=None):
            if isinstance(r, dict):
                return r.get(key, default)
            return getattr(r, key, default)
        user_id_list_join = str(get_val(activity, 'user_id_list_join', ''))
        if not activity or not user_id_list_join:
            return False, "Activity not found or you are not a participant."
        joined_ids = [uid.strip() for uid in user_id_list_join.split(",") if uid.strip()]
        if str(user_id) in joined_ids:
            joined_ids.remove(str(user_id))
            new_join_list = ",".join([str(uid) for uid in joined_ids])
            update_sports_activity(activity_id, new_join_list)
            return True, "You have left the activity."
        else:
            return False, "You are not a participant in this activity."

    def delete_post(self, user_id, post_id):
        success = deletePost(user_id, post_id)
        if success:
            return True, "Post deleted successfully."
        else:
            return False, "Failed to delete post."

    def generate_otp(self, user_id):
        otp_data, error = generate_otp_for_user(user_id)
        if error:
            return None, error
        return otp_data, None

    def verify_otp(self, user_id, otp_code):
        success, error = verify_and_enable_otp(user_id, otp_code)
        return success, error

    def check_otp_status(self, user_id):
        user_data = get_user_by_id(user_id)
        otp_enabled = False
        if user_data:
            if isinstance(user_data, dict):
                otp_enabled = user_data.get("otp_enabled", False)
            else:
                otp_enabled = getattr(user_data, "otp_enabled", False)
        return bool(otp_enabled)
