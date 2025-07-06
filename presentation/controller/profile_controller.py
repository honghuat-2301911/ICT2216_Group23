import os
import uuid

import bcrypt
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from domain.control.profile_management import ProfileManagement
from domain.entity.forms import (
    ActivityEditForm,
    DeleteForm,
    PostEditForm,
    ProfileEditForm,
    DisableOTPForm,
)

profile_bp = Blueprint(
    "profile_bp",
    __name__,
    template_folder="../templates/profile",
    url_prefix="/profile",
)

@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def fetchProfile():
    user_id = int(current_user.get_id())
    profile_manager = ProfileManagement()
    user = profile_manager.get_user_profile(user_id)
    user_posts = profile_manager.get_user_posts(user_id)
    hosted_activities, joined_only_activities = profile_manager.get_user_activities(user_id)
    form = ProfileEditForm(obj=user)
    if request.method == "POST" and form.validate_on_submit():
        result = profile_manager.update_profile_full(user_id, form)
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile_bp.fetchProfile"))
    return render_template(
        "profile/profile.html",
        user=user,
        posts=user_posts,
        hosted_activities=hosted_activities,
        joined_only_activities=joined_only_activities,
        profile_form=form,
        activity_form=ActivityEditForm(),
        post_form=PostEditForm(),
        delete_form=DeleteForm(),
    )

@profile_bp.route("/edit_activity/<int:activity_id>", methods=["POST"])
@login_required
def edit_activity(activity_id):
    user_id = int(current_user.get_id())
    form = ActivityEditForm()
    profile_manager = ProfileManagement()
    success, message = profile_manager.edit_activity(user_id, activity_id, form)
    flash(message, "success" if success else "danger")
    return redirect(url_for("profile_bp.fetchProfile") + "#activitiesSection")

@profile_bp.route("/edit_post/<int:post_id>", methods=["POST"])
@login_required
def edit_post(post_id):
    user_id = int(current_user.get_id())
    form = PostEditForm()
    profile_manager = ProfileManagement()
    success, message = profile_manager.edit_post(user_id, post_id, form)
    flash(message, "success" if success else "danger")
    return redirect(url_for("profile_bp.fetchProfile") + "#feedSection")

@profile_bp.route("/leave_activity/<int:activity_id>", methods=["POST"])
@login_required
def leave_activity(activity_id):
    user_id = int(current_user.get_id())
    profile_manager = ProfileManagement()
    success, message = profile_manager.leave_activity(user_id, activity_id)
    flash(message, "success" if success else ("warning" if "not a participant" in message else "danger"))
    return redirect(url_for("profile_bp.fetchProfile") + "#activitiesSection")

@profile_bp.route("/delete_post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    user_id = int(current_user.get_id())
    profile_manager = ProfileManagement()
    success, message = profile_manager.delete_post(user_id, post_id)
    flash(message, "success" if success else "danger")
    return redirect(url_for("profile_bp.fetchProfile") + "#feedSection")

@profile_bp.route("/joined_users/<int:activity_id>", methods=["GET"])
@login_required
def get_joined_users(activity_id):
    profile_manager = ProfileManagement()
    users = profile_manager.get_joined_user_names(activity_id)
    return jsonify(users)

@profile_bp.route("/generate_otp", methods=["POST"])
@login_required
def generate_otp():
    try:
        user_id = int(current_user.get_id())
        profile_manager = ProfileManagement()
        otp_data, error = profile_manager.generate_otp(user_id)
        if error or not otp_data:
            return jsonify({"status": "error", "message": error or "Failed to generate OTP data"}), 400
        return jsonify({"status": "success", "qr": otp_data["qr"], "secret": otp_data["secret"]})
    except Exception as e:
        current_app.logger.error(f"OTP generation error: {str(e)}")
        return (
            jsonify({"status": "error", "message": "Failed to generate OTP setup"}),
            500,
        )

@profile_bp.route("/verify_otp", methods=["POST"])
@login_required
def verify_otp():
    try:
        user_id = int(current_user.get_id())
        if not request.json or "otp_code" not in request.json:
            return jsonify({"status": "error", "message": "OTP code not provided"}), 400
        otp_code = request.json.get("otp_code")
        profile_manager = ProfileManagement()
        success, error = profile_manager.verify_otp(user_id, otp_code)
        if success:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": error}), 400
    except Exception as e:
        current_app.logger.error(f"OTP verification error: {str(e)}")
        return jsonify({"status": "error", "message": "Failed to verify OTP"}), 500

@profile_bp.route("/disable_otp", methods=["POST"])
@login_required
def disable_otp_route():
    user_id = int(current_user.get_id())
    profile_manager = ProfileManagement()
    success = profile_manager.disable_otp(user_id)
    if success:
        flash("OTP has been disabled.", "success")
    else:
        flash("Failed to disable OTP.", "danger")
    return redirect(url_for("profile_bp.fetchProfile"))