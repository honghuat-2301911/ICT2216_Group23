import profile
from flask import Blueprint, render_template, request, redirect, url_for
from data_source.social_feed_queries import get_posts_by_user
from data_source.bulletin_feed_queries import get_all_activities

profile_bp = Blueprint('profile_bp', __name__, template_folder='../templates/profile', url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
def view_profile():
    # Example: Replace this with actual user fetching logic (e.g., from session or database)
    user = {
        "userId": 1,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "skill_lvl": "Intermediate",
        "sports_exp": "2 years"
    }
    user_posts = get_posts_by_user(user["name"])
    # Filter activities where userId is in user_id_list_join
    all_activities = get_all_activities()
    user_id_str = str(user["userId"])
    joined_activities = [
        a for a in all_activities
        if user_id_str in [uid.strip() for uid in (a["user_id_list_join"].split(",") if a["user_id_list_join"] else [])]
        or a["user_id"] == user["userId"]
    ]
    return render_template('profile/profile.html', user=user, posts=user_posts, joined_activities=joined_activities)

@profile_bp.route('/', methods=['POST'])
def edit_profile():
    # TODO: Handle profile update logic
    return redirect(url_for('profile_bp.view_profile')) 