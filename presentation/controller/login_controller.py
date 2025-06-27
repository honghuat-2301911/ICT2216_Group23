"""Controller for user authentication and login functionality"""

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from domain.control.login_management import get_user_display_data, login_user, logout_user

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
    if current_user.is_authenticated:
        return redirect(url_for("bulletin.bulletin_page"))
    if request.method == "POST":
        user = login_user(request.form["email"], request.form["password"])
        if user:
            return redirect(url_for("bulletin.bulletin_page"))
        else:
            return render_template("login/login.html", error="Login failed.")
    return render_template("login/login.html")


@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.login"))
