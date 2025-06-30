import functools  # Import functools

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from domain.control.admin_management import *
from domain.control.bulletin_management import *

# Create a blueprint for the admin page
admin_bp = Blueprint(
    "admin", __name__, url_prefix="/admin", template_folder="../templates"
)


def admin_required(func):
    """
    Custom decorator to check if the current user is authenticated and is an admin.
    This decorator should only be used to protect admin routes.
    """

    @functools.wraps(func)
    def admin_check(*args, **kwargs):
        # Check if the user is logged in and is an admin
        if not current_user.is_authenticated or current_user.role != "admin":
            # Redirect to a different page if not admin
            return redirect(url_for("bulletin.bulletin_page"))
        return func(
            *args, **kwargs
        )  # Call the original function if authenticated as admin

    return admin_check  # Return the wrapped function


@admin_bp.route("/bulletin", methods=["GET", "POST"])
@login_required
@admin_required
def bulletin_page():
    query = request.form.get("query") if request.method == "POST" else None
    if query:
        result = search_bulletin(query)
    else:
        result = get_bulletin_listing()
    if not result:
        return render_template(
            "admin/bulletin.html", bulletin_list=[], error="No activities found."
        )
    bulletin_list = get_bulletin_display_data()
    return render_template("admin/bulletin.html", bulletin_list=bulletin_list)


@admin_bp.route("/delete_activity", methods=["POST"])
@login_required
@admin_required
def delete_activity():
    activity_id = request.form.get("activity_id")
    if not activity_id:
        flash("Activity ID is required.", "error")
        return redirect(url_for("admin.bulletin_page"))

    success = remove_sports_activity(
        activity_id
    )  # <-- Double-check which delete_activity this refers to
    if success:
        flash("Activity deleted successfully.", "success")
    else:
        flash(
            "Failed to delete the activity. It may not exist or you may not have permission.",
            "error",
        )

    return redirect(url_for("admin.bulletin_page"))
