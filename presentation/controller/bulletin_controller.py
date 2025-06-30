from flask import Blueprint, redirect, render_template, session, url_for, request, flash
from domain.control.bulletin_management import *
from flask_login import login_required, current_user
import functools 

# Create a blueprint for the bulletin page
bulletin_bp = Blueprint(
    "bulletin",
    __name__,
    url_prefix="/",
    template_folder="../templates"
)

def user_required(func):
    """
    Decorator to ensure the current_user is logged in AND has role 'user'.
    Admins (or anyone else) will be redirected away.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'user':
            flash("You do not have permission to access that page.", "error")
            return redirect(url_for("bulletin.bulletin_page"))
        return func(*args, **kwargs)
    return wrapper


@bulletin_bp.route("/bulletin", methods=["GET", "POST"])
@login_required
@user_required
def bulletin_page():
    """Render the bulletin board page if the user is logged in.

    Redirects to the login page if the user is not authenticated.
    """
    # # Check if user is logged in
    # if "user_id" not in session:
    #     return redirect(url_for("login.login"))
    # need validation here for query lol

    query = request.form.get("query") if request.method == "POST" else None
    if query:
        result = search_bulletin(query)
    else:
        result = get_bulletin_listing()
    if not result:  
        return render_template("bulletin/bulletin.html", bulletin_list=[], error="No activities found.")
    bulletin_list = get_bulletin_display_data()
    return render_template("bulletin/bulletin.html", bulletin_list=bulletin_list, query=query)
        

@bulletin_bp.route("/join", methods=["POST"])
@login_required
@user_required
def join_activity():
    activity_id = request.form.get("activity_id")
    result = join_activity_control(activity_id)
    if not result:
        #flash ("Failed to join the activity You Joined Already Please try again.")
        return redirect(url_for("bulletin.bulletin_page"))
    return redirect(url_for("bulletin.bulletin_page"))

@bulletin_bp.route("/host", methods=["POST"])
@login_required
def host_activity():
    activity_name = request.form["activity_name"]
    activity_type = request.form["activity_type"]
    skills_req = request.form["skills_req"]
    date = request.form["date"]
    location = request.form["location"]
    max_pax = request.form["max_pax"]

    success = create_activity(activity_name, activity_type, skills_req, date, location, max_pax)

    if success:
        return redirect(url_for("bulletin.bulletin_page"))
    return redirect(url_for("bulletin.bulletin_page"))

@bulletin_bp.route("/bulletin/filtered", methods=["POST"])
@login_required
def filtered_bulletin():
    sports_checked = request.form.get("sports_checkbox") == "on"
    non_sports_checked = request.form.get("non_sports_checkbox") == "on"

    if not sports_checked and not non_sports_checked:
        return render_template("bulletin/bulletin.html", bulletin_list=[], error="Please select at least one category to filter.")
    result = get_filtered_bulletins(sports_checked, non_sports_checked)
    if not result:
        return render_template("bulletin/bulletin.html", bulletin_list=[], error="No activities found for the selected categories.")
    
    bulletin_list = get_bulletin_display_data()
    return render_template("bulletin/bulletin.html", bulletin_list=bulletin_list)


