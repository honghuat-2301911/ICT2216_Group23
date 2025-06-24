from flask import Blueprint, redirect, render_template, session, url_for

# Create a blueprint for the bulletin page
bulletin_bp = Blueprint(
    "bulletin",
    __name__,
    url_prefix="/bulletin",
    template_folder="../templates"
)

@bulletin_bp.route("/")
def bulletin():

    return render_template("bulletin/bulletin.html")
