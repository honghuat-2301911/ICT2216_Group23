import profile
from flask import Blueprint, render_template, request, redirect, url_for

profile_bp = Blueprint('profile_bp', __name__, template_folder='../templates/profile', url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
def view_profile():
    # Example: Replace this with actual user fetching logic (e.g., from session or database)
    user = {
        "userId": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "skill_lvl": "Intermediate",
        "sports_exp": "3 years"
    }
    return render_template('profile/profile.html', user=None)

@profile_bp.route('/', methods=['POST'])
def edit_profile():
    # TODO: Handle profile update logic
    return redirect(url_for('profile_bp.view_profile')) 