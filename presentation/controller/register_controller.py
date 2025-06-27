"""Controller for user registration functionality"""

import random
import bcrypt

from flask import Blueprint, redirect, render_template, request, url_for

from domain.control.register import register_user

register_bp = Blueprint(
    "register", __name__, url_prefix="/", template_folder="../templates/"
)


@register_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration requests.

    GET: Show registration form
    POST: Process registration data
    """
    if request.method == "POST":
        # Validate password match
        if request.form["password"] != request.form["confirm_password"]:
            return redirect(url_for("register.register"))
        # Handle form submission
        # hashed_password = hash_password(request.form["password"])

        # Prepare user data
        user_data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            "skill_lvl": request.form.get("skill_lvl"),
            "sports_exp": request.form.get("sports_exp"),
            "role": "user",
        }

        # Attempt registration
        if register_user(user_data):
            return redirect(url_for("login.login"))
        return redirect(url_for("register.register"))

    # Show registration form for GET requests
    return render_template("register/register.html")
