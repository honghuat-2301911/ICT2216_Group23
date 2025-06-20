from flask import Blueprint, redirect, render_template, session, url_for

# Create a blueprint for the bulletin page
bulletin_bp = Blueprint(
    "bulletin",
    __name__,
    url_prefix="/bulletin",
    template_folder="../templates"
)

@bulletin_bp.route("/")
def bulletin_page():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    return render_template("bulletin/bulletin.html")
