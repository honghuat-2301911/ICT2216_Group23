import profile
from flask import Blueprint, render_template, request, redirect, url_for
from data_source.social_feed_queries import get_posts_by_user
from data_source.bulletin_feed_queries import get_all_activities
from data_source.user_queries import get_user_by_email, update_user_profile, get_user_by_id, update_user_profile_by_id

profile_bp = Blueprint('profile_bp', __name__, template_folder='../templates/profile', url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
def view_profile():
    user_id = 159
    user = get_user_by_id(user_id)
    user_posts = get_posts_by_user(user['name']) if user else []
    all_activities = get_all_activities()
    user_id_str = str(user['id']) if user else ''
    joined_activities = [
        a for a in all_activities
        if user_id_str in [uid.strip() for uid in (a["user_id_list_join"].split(",") if a["user_id_list_join"] else [])]
        or a["user_id"] == user['id']
    ] if user else []
    return render_template('profile/profile.html', user=user, posts=user_posts, joined_activities=joined_activities)

@profile_bp.route('/', methods=['POST'])
def edit_profile():
    user_id = 159
    name = request.form['name']
    password = request.form['password'] or None
    print("Updating user:", user_id, name, password)
    result = update_user_profile_by_id(user_id, name, password)
    print("Update result:", result)
    return redirect(url_for('profile_bp.view_profile'))