import bcrypt
from flask import Blueprint, redirect, render_template, flash, url_for
from domain.entity.forms import RegisterForm
from domain.control.register import register_user


register_bp = Blueprint(
    "register", __name__,
    url_prefix="/",
    template_folder="../templates/"
)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Prepare user data
        hashed = bcrypt.hashpw(
            form.password.data.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user_data = {
            "name": form.name.data,
            "email": form.email.data,
            "password": hashed,
            "skill_lvl": form.skill_lvl.data,
            "sports_exp": form.sports_exp.data,
            "role": "user",
        }

        if register_user(user_data):
            flash("Registration successful", "success")
            return redirect(url_for("login.login"))

        flash("Something went wrong. Please try again.", "error")
        return redirect(url_for("register.register"))

    # If GET or validation failed, render form with errors
    return render_template("register/register.html", form=form)
