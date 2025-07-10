import os
from datetime import datetime, timezone

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required
from flask_login import login_user as flask_login_user
from flask_login import logout_user as flask_logout_user
from itsdangerous import URLSafeTimedSerializer

from data_source.user_queries import (
    get_user_by_email,
    get_user_session_token,
    update_user_session_token,
)
from domain.control.login_management import (
    get_user_display_data,
    login_user,
    logout_user,
    process_reset_password,
    process_reset_password_request,
    verify_control_class,
    verify_otp_control_class,
    verify_user_otp,
)
from domain.entity.forms import LoginForm, OTPForm, RequestResetForm, ResetPasswordForm
from domain.entity.user import User

LOGIN_VIEW = "login.login"
BULLETIN_PAGE = "bulletin.bulletin_page"

login_bp = Blueprint(
    "login", __name__, url_prefix="/", template_folder="../templates/login"
)


def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr


@login_bp.route("/")
def root_redirect():
    return redirect(url_for(LOGIN_VIEW))


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(BULLETIN_PAGE))

    form = LoginForm()
    if form.validate_on_submit():
        # use form data
        user = login_user(form.email.data, form.password.data)
        if user:
            # Check if email is verified
            if not getattr(user, "email_verified", False):
                form.email.errors.append(
                    "You must verify your email before logging in. Please check your inbox."
                )
                current_app.logger.warning(
                    f"Unverified login attempt by user with email: {form.email.data}"
                )
                return render_template("login/login.html", form=form)
            # If 2FA is enabled, redirect to OTP verification page
            if getattr(user, "otp_enabled", False):
                session["pre_2fa_user_id"] = user.id
                session["pre_2fa_user_email"] = user.email
                return redirect(url_for("login.otp_verify"))
            # Else perform normal login
            session.clear()
            flask_login_user(user)

            session["init"] = os.urandom(16).hex()
            session_token = os.urandom(32).hex()
            session["session_token"] = session_token
            update_user_session_token(user.id, session_token)
            session["created_at"] = datetime.now(timezone.utc).isoformat()
            session["last_activity"] = datetime.now(timezone.utc).isoformat()

            session.modified = True
            
            if user.role == "admin":
                current_app.logger.info(
                    f"Admin user with email: {form.email.data} was logged in successfully"
                )
                return redirect(url_for("admin.bulletin_page"))
            else:
                current_app.logger.info(
                    f"Normal user with email: {form.email.data} was logged in successfully"
                )
                return redirect(url_for(BULLETIN_PAGE))
        # invalid credentials
        form.email.errors.append("Invalid email or password.")
    # either GET or validation failed
    return render_template("login/login.html", form=form)


@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    if hasattr(current_user, "id"):
        current_app.logger.info(f"User with ID {current_user.id} logged out")
        update_user_session_token(current_user.id, None)
    session.clear()
    return redirect(url_for(LOGIN_VIEW))


@login_bp.route("/otp_verify", methods=["GET", "POST"])
def otp_verify():
    user_id = session.get("pre_2fa_user_id")
    user_email = session.get("pre_2fa_user_email")
    if not user_id or not user_email:
        return redirect(url_for(LOGIN_VIEW))
    result = verify_control_class(user_email)
    if not result:
        flash("OTP setup not found. Please login again.")
        return redirect(url_for(LOGIN_VIEW))
    form = OTPForm()
    if form.validate_on_submit():
        verified, user = verify_otp_control_class(user_email, form)
        if verified:
            session.clear()  # Force new session after 2FA so that hackers cannot use the same session ID even in 2FA fails
            session["init"] = os.urandom(16).hex()  # Force new session file/ID
            session_token = os.urandom(32).hex()
            session["session_token"] = session_token
            update_user_session_token(user.id, session_token)
            flask_login_user(user)
            session.pop("pre_2fa_user_id", None)
            session.pop("pre_2fa_user_email", None)
            session["created_at"] = datetime.now(timezone.utc).isoformat()
            session["last_activity"] = datetime.now(timezone.utc).isoformat()
            if user.role == "admin":
                current_app.logger.info(
                    f"Admin User with email {user.email} passed 2FA and was logged in"
                )
                return redirect(url_for("admin.bulletin_page"))
            else:
                current_app.logger.info(
                    f"Normal User with email {user.email} passed 2FA and was logged in"
                )
                return redirect(url_for(BULLETIN_PAGE))
        else:
            ip = get_client_ip()
            current_app.logger.warning(
                f"Failed OTP verification attempt for user: {user.email}, IP: {ip}"
            )
            flash("Invalid OTP code. Please try again.")
    return render_template("login/login_otp.html", form=form)


@login_bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        process_reset_password_request(form.email.data)
        flash(
            "If your email is registered, you will receive a password reset link.",
            "info",
        )
        return redirect(url_for("login.login"))
    return render_template("reset_password_request.html", form=form)


@login_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()
    return process_reset_password(token, form)
