from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from domain.control.register import *
import random

register_bp = Blueprint(
    "register",
    __name__,
    url_prefix="/",
    template_folder="../templates/"
)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["password"] != request.form["confirm_password"]:
            return redirect(url_for("register.register"))   
        # Handle form submission
        # hashed_password = hash_password(request.form["password"])
        user_data = {
            "id": random.randint(5,200), #THIS IS JUST A TEMP ID, IS STUDENTS WILL NEED TO CHANGE THIS, edit init.sql if needed for schema changes
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"],
            "skill_lvl": request.form.get("skill_lvl"),
            "sports_exp": request.form.get("sports_exp"),
            "role": "user"
        }

        if register_user(user_data):
            return redirect(url_for("login.login"))
        else:
            return redirect(url_for("register.register"))

    # If GET request, show the registration form
    return render_template("register/register.html")
