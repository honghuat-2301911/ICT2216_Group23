from flask import Blueprint, render_template, request, redirect, url_for, session
from domain.control.login_management import *

# Create a blueprint for all main routes
login_bp = Blueprint(
    "login",
    __name__,
    url_prefix="/",
    template_folder="../templates"
)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        if not email or not password:
            return render_template("login/login.html", error="Please fill in all fields")
        
        if email == "test@example.com" and password == "password123":
            # session['user_id'] = 1
            # session['email'] = email
            # if remember:
            #     session.permanent = True
            
            return redirect(url_for('login.bulletin'))
        else:
            return render_template("login/login.html", error="Invalid email or password.")
    
    return render_template("login/login.html")

@login_bp.route("/register", methods=["GET", "POST"])
def register():
    # You can add registration logic here
    return render_template("register/register.html")

@login_bp.route("/bulletin")
def bulletin():
    # if 'user_id' not in session:
    #     return redirect(url_for('login.login'))
    return render_template("bulletin/bulletin.html")

@login_bp.route("/logout")
def logout():
    # session.clear()
    return redirect(url_for('login.login'))

