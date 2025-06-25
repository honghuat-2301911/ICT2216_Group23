from flask import Blueprint, redirect, render_template, session, url_for, request, flash
from domain.control.bulletin_management import *
# Create a blueprint for the bulletin page
bulletin_bp = Blueprint(
    "bulletin",
    __name__,
    url_prefix="/",
    template_folder="../templates"
)

@bulletin_bp.route("/bulletin", methods=["GET", "POST"])
def bulletin_page():
    # # Check if user is logged in
    # if 'user_id' not in session:
    #     return redirect(url_for('login.login'))
    # need validation here for query lol

    query = request.form.get("query") if request.method == "POST" else None
    if query:
        result = search_bulletin(query)
    else:
        result = get_bulletin_listing()
    if not result:  
        return render_template("bulletin/bulletin.html", bulletin_list=[], error="No activities found.")
    bulletin_list = get_bulletin_display_data()
    return render_template("bulletin/bulletin.html", bulletin_list=bulletin_list)
        

@bulletin_bp.route("/join", methods=["POST"])
def join_activity():
    activity_id = request.form.get("activity_id")
    result = join_activity_control(activity_id)
    if not result:
        #flash ("Failed to join the activity You Joined Already Please try again.")
        return redirect(url_for("bulletin.bulletin_page"))
    return redirect(url_for("bulletin.bulletin_page"))

@bulletin_bp.route("/host", methods=["POST"])
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


