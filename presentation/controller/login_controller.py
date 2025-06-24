"""Controller for user authentication and login functionality"""

from flask import Blueprint, redirect, render_template, request, url_for

from domain.control.login_management import get_user_display_data, login_user

login_bp = Blueprint(
    "login", __name__, url_prefix="/", template_folder="../templates/login"
)


@login_bp.route("/")
def root_redirect():
    """Redirect root path to login page"""
    return redirect(url_for("login.login"))


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login requests

    GET: Show login form
    POST: Process login credentials
    """
    if request.method == "POST":
        user = login_user(request.form["email"], request.form["password"])
        if user:
            result = get_user_display_data()
            return render_template("login/login.html", user=result)
        return render_template("login/login.html", error="Login failed.")
    return render_template("login/login.html")
