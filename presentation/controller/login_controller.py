from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from domain.control.login_management import *

login_bp = Blueprint(
    "login",
    __name__,
    url_prefix="/",
    template_folder="../templates/login"
)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    # ggs@gg.com is just for testing, u have to get input from form in login.html.
    # insert a new record in user table in mysql and then put the same email and password here to test login
    user = login_user("ggs@gg.com", "123")
    if user:
        # Create a safe user dictionary to avoid exposing sensitive data
        safe_user = {
            "name": user.get_name(),
            "email": user.get_email(),
            "skill_lvl": user.get_skill_lvl(),
            "sports_exp": user.get_sports_exp(),
        }
        #just change render to maybe profile page and see if can display on ur html by right need session
        return render_template("login/login.html", user=safe_user)
    else:
        return render_template("login/login.html", error="Login failed.")


