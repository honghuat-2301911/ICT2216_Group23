from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from domain.control.login_management import *

login_bp = Blueprint(
    "login", __name__, url_prefix="/", template_folder="../templates/login"
)


@login_bp.route("/")
def root_redirect():
    return redirect(url_for("login.login"))


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    # ggs@gg.com is just for testing, u have to get input from form in login.html.
    # insert a new record in user table in mysql and then put the same email and password here to test login
    if request.method == "POST":
        user = login_user(request.form["email"], request.form["password"])
        if user:
            result = get_user_display_data()
            return render_template("login/login.html", user=result)
        else:
            return render_template("login/login.html", error="Login failed.")
    return render_template("login/login.html")
