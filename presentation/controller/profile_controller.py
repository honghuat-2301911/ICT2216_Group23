from flask import Blueprint, render_template, request, redirect, url_for
from domain.control.profile_management import ProfileManagement
from domain.entity.user import User
from data_source.social_feed_queries import get_posts_by_user
from data_source.user_queries import get_user_by_id
from flask_login import login_required, current_user
import bcrypt

profile_bp = Blueprint('profile_bp', __name__, template_folder='../templates/profile', url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
@login_required
def fetchProfile():
    user_id = int(current_user.get_id())
    user_data = get_user_by_id(user_id)
    user = None
    if isinstance(user_data, dict):
        id_val = user_data.get('id')
        if isinstance(id_val, int):
            user_id_val = id_val
        elif isinstance(id_val, str) and id_val.isdigit():
            user_id_val = int(id_val)
        else:
            user_id_val = 0
        user = User(
            user_id_val,
            str(user_data.get('name')) if user_data.get('name') is not None else '',
            str(user_data.get('password')) if user_data.get('password') is not None else '',
            str(user_data.get('email')) if user_data.get('email') is not None else '',
            str(user_data.get('role', 'user'))
        )
    user_posts = get_posts_by_user(user.get_name()) if user else []
    user_id_str = str(user.get_id()) if user else ''
    joined_activities = []  # No activities since get_all_activities is removed
    return render_template('profile/profile.html', user=user, posts=user_posts, joined_activities=joined_activities)


@profile_bp.route('/', methods=['POST'])
@login_required
def editProfile():
    user_id = int(current_user.get_id())
    name = request.form['name']
    password = request.form['password']
    profile_manager = ProfileManagement()
    if password:
        # Hash the new password before saving
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        result = profile_manager.updateProfile(user_id, name, hashed_password)
    else:
        # Fetch current password from DB
        user_data = get_user_by_id(user_id)
        current_password = user_data['password'] if isinstance(user_data, dict) and 'password' in user_data else ''
        result = profile_manager.updateProfile(user_id, name, current_password)
    return redirect(url_for('profile_bp.fetchProfile'))