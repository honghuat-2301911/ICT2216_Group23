from flask import Blueprint, render_template, request, redirect, url_for
from domain.control.profile_management import ProfileManagement
from domain.entity.user import User
from data_source.social_feed_queries import get_posts_by_user
from data_source.bulletin_feed_queries import get_all_activities
from data_source.user_queries import get_user_by_id

profile_bp = Blueprint('profile_bp', __name__, template_folder='../templates/profile', url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
def fetchProfile():
    user_id = 159  # TODO: Replace with session or request user id
    user_data = get_user_by_id(user_id)
    user = None
    if isinstance(user_data, dict):
        user = User(
            user_data.get('id'),
            user_data.get('name'),
            user_data.get('password'),
            user_data.get('email'),
            user_data.get('skill_lvl'),
            user_data.get('sports_exp'),
            str(user_data.get('role', 'user'))
        )
    user_posts = get_posts_by_user(user.get_name()) if user else []
    all_activities = get_all_activities()
    user_id_str = str(user.get_id()) if user else ''
    joined_activities = [
        a for a in all_activities
        if user_id_str in [uid.strip() for uid in (a["user_id_list_join"].split(",") if a["user_id_list_join"] else [])]
        or a["user_id"] == user.get_id()
    ] if user else []
    return render_template('profile/profile.html', user=user, posts=user_posts, joined_activities=joined_activities)

# ECB: Boundary (Controller) - editProfile
@profile_bp.route('/', methods=['POST'])
def editProfile():
    user_id = 159  # TODO: Replace with session or request user id
    name = request.form['name']
    password = request.form['password'] or None
    profile_manager = ProfileManagement()
    result = profile_manager.updateProfile(user_id, name, password)
    return redirect(url_for('profile_bp.fetchProfile'))