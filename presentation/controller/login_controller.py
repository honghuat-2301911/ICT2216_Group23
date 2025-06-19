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
    text = test_print_user(1, "gg@gg.com", "123", "LeBron")
    return render_template("login/login.html", text=text)

