"""User login management for authentication and session handling"""

from datetime import datetime, timedelta, timezone

import bcrypt
import pyotp
from flask import current_app, g, url_for,flash, redirect, render_template
from flask_login import login_user as flask_login_user
from flask_login import logout_user as flask_logout_user
from itsdangerous import URLSafeTimedSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import bcrypt
import os

from data_source.user_queries import (
    clear_failed_logins,
    get_user_by_email,
    get_user_failed_attempts_count,
    record_failed_login,
    update_user_lockout,
    update_user_password_by_email,
)
from domain.entity.user import User

FAILED_ATTEMPT_LIMIT = 10
LOCKOUT_MINUTES = 15


def login_user(email: str, password: str):
    """
    Attempt to authenticate a user by email and password

    Args:
        email (str): User's email address
        password (str): User's password

    Returns:
        User: The authenticated User object if found, else None
    """
    result = get_user_by_email(email)
    if not result:
        return None

    # Get current time
    utc_plus_8 = timezone(timedelta(hours=8))
    now = datetime.now(utc_plus_8)

    # Check if account is locked
    if result.get("locked_until"):
        db_locked_until = result["locked_until"].replace(tzinfo=utc_plus_8)
        if db_locked_until > now:
            lock_time = db_locked_until.strftime("%Y-%m-%d %H:%M:%S")
            current_app.logger.warning(
                f"Locked account login attempt: {email} (locked until {lock_time})"
            )
            return None

    # Check password hash
    stored_hash = result["password"]
    password_valid = bcrypt.checkpw(
        password.encode("utf-8"), stored_hash.encode("utf-8")
    )

    # If password doesn't match, log failed attempt into DB
    if not password_valid:
        record_failed_login(result["id"])
        # Check failed attempts in past 10 minutes
        recent_failures = get_user_failed_attempts_count(
            result["id"], window_minutes=10
        )
        locked_until = None
        if recent_failures >= FAILED_ATTEMPT_LIMIT:
            locked_until = now + timedelta(minutes=LOCKOUT_MINUTES)
            update_user_lockout(result["id"], locked_until.replace(tzinfo=None))
            current_app.logger.warning(
                f"Account locked: {email} after {recent_failures} failed attempts in 10 minutes"
            )
        current_app.logger.warning(
            f"Failed login for {email} (attempt {recent_failures}/{FAILED_ATTEMPT_LIMIT})"
        )
        return None

    # On successful login, clear failed logins and unlock account
    clear_failed_logins(result["id"])
    update_user_lockout(result["id"], None)

    user = User(
        id=result["id"],
        name=result["name"],
        password=result["password"],
        email=result["email"],
        role=result.get("role", "user"),
        profile_picture=result.get("profile_picture", ""),
        locked_until=result.get("locked_until"),
        otp_secret=result.get("otp_secret"),
        otp_enabled=bool(int(result.get("otp_enabled", 0))),
        current_session_token=result.get("current_session_token"),
        email_verified=bool(int(result.get("email_verified", 0))),
    )
    # flask_login_user(user)
    return user


# Get generate OTP
def verify_user_otp(user, otp_code):
    """
    Verifies the OTP code for the user.
    Args:
        user (User): The user object
        otp_code (str): The OTP code entered by the user
    Returns:
        bool: True if valid, False otherwise
    """
    if not user.otp_secret:
        return False
    totp = pyotp.TOTP(user.otp_secret)
    return totp.verify(otp_code)


def logout_user():
    """Log out the current user using flask_login"""
    flask_logout_user()


def get_user_display_data():
    """
    Retrieve display data for the currently logged-in user

    Returns:
        dict: User display information, or None if no user is logged in
    """
    user = g.get("current_user")
    if not user:
        return None

    return {
        # "id": user.get_id(),  # Uncomment if you want to display user ID
        "name": user.get_name(),
        "email": user.get_email(),
        "role": user.get_role(),
    }

def process_reset_password_request(email):
    user = get_user_by_email(email)
    if user:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(user['email'], salt='password-reset')

        # Send the reset email with the token
        reset_url = url_for('login.reset_password', token=token, _external=True)
        message = Mail(
            from_email='buddiesfinder@gmail.com',
            to_emails=email,
            subject='Reset Your Password for buddiesfinder',
            html_content=f'<p>Click <a href="{reset_url}">here</a> to reset your password.</p>'
        )
        try:
            api_key = os.getenv('EMAILVERIFICATION_API_KEY')
            sg = SendGridAPIClient(api_key)
            sg.send(message)       
        except Exception as e:
            current_app.logger.error(f"Error sending verification email: {e}")


def process_reset_password(token, form):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except (SignatureExpired, BadSignature):
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.reset_password_request'))

    if form.validate_on_submit():
        hashed = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = get_user_by_email(email)
        if user:
            update_user_password_by_email(user['email'], hashed)
            flash('Your password has been updated. You can now log in.', 'success')
            return redirect(url_for('login.login'))
    return render_template('reset_password.html', form=form)