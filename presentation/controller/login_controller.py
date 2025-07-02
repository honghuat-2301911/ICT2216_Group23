from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from flask_login import login_user as flask_login_user
from flask_login import logout_user as flask_logout_user
from domain.entity.forms import OTPForm 

from data_source.user_queries import get_user_by_email
from domain.control.login_management import (
    get_user_display_data,
    login_user,
    logout_user,
    verify_user_otp,
)
from domain.entity.forms import LoginForm
from domain.entity.user import User

login_bp = Blueprint(
    "login", __name__, url_prefix="/", template_folder="../templates/login"
)


@login_bp.route("/")
def root_redirect():
    return redirect(url_for("login.login"))


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bulletin.bulletin_page"))

    form = LoginForm()
    if form.validate_on_submit():
        # use form data
        user = login_user(form.email.data, form.password.data)
        if user:
            # If 2FA is enabled, redirect to OTP verification page
            if getattr(user, "otp_enabled", False):
                session["pre_2fa_user_id"] = user.id
                session["pre_2fa_user_email"] = user.email
                return redirect(url_for("login.otp_verify"))
            # Else perform normal login
            flask_login_user(user)
            if user.role == "admin":
                return redirect(url_for("admin.bulletin_page"))
            else:
                return redirect(url_for("bulletin.bulletin_page"))
        # invalid credentials
        form.email.errors.append("Invalid email or password.")
    # either GET or validation failed
    return render_template("login/login.html", form=form)


@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("_flashes", None)
    return redirect(url_for("login.login"))


@login_bp.route("/otp_verify", methods=["GET", "POST"])
def otp_verify():
    user_id = session.get("pre_2fa_user_id")
    user_email = session.get("pre_2fa_user_email")
    if not user_id or not user_email:
        return redirect(url_for("login.login"))
    user_data = get_user_by_email(user_email)
    if not user_data or not user_data.get("otp_secret"):
        flash("OTP setup not found. Please login again.")
        return redirect(url_for("login.login"))

    form = OTPForm()
    if form.validate_on_submit():
        otp_code = form.otp_code.data
        from domain.entity.user import User
        user = User(
            id=user_data["id"],
            name=user_data["name"],
            password=user_data["password"],
            email=user_data["email"],
            role=user_data.get("role", "user"),
            profile_picture=user_data.get("profile_picture", ""),
            otp_secret=user_data.get("otp_secret"),
            otp_enabled=bool(int(user_data.get("otp_enabled", 0))),
        )
        verified = verify_user_otp(user, otp_code)
        if verified:
            flask_login_user(user)
            session.pop("pre_2fa_user_id", None)
            session.pop("pre_2fa_user_email", None)
            if user.role == "admin":
                return redirect(url_for("admin.bulletin_page"))
            else:
                return redirect(url_for("bulletin.bulletin_page"))
        else:
            flash("Invalid OTP code. Please try again.")
    return render_template("login/login_otp.html", form=form)
