import os

from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from flask_wtf import CSRFProtect

from data_source.user_queries import get_user_by_id
from domain.entity.user import User
from presentation.controller.admin_controller import admin_bp
from presentation.controller.bulletin_controller import bulletin_bp
from presentation.controller.login_controller import login_bp
from presentation.controller.profile_controller import profile_bp
from presentation.controller.register_controller import register_bp
from presentation.controller.social_feed_controller import social_feed_bp

# from data_source.login_queries import init_schema


def create_app():
    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
        static_url_path="/static",
    )
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "")
    app.config["SESSION_TYPE"] = "filesystem"

    # # Only send cookies over HTTPS
    # app.config['SESSION_COOKIE_SECURE']   = True
    # # Prevent JavaScript from reading the cookie
    # app.config['SESSION_COOKIE_HTTPONLY'] = True
    # # Control cross-site sending; options: 'Lax', 'Strict', or 'None'
    # app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # app.config['REMEMBER_COOKIE_SECURE']   = True
    # app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    # app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

    Session(app)

    login_manager = LoginManager()
    login_manager.login_view = "login.login"
    login_manager.init_app(app)

    # csrf = CSRFProtect(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_data = get_user_by_id(user_id)
        if user_data:
            return User(
                id=user_data["id"],
                name=user_data["name"],
                password=user_data["password"],
                email=user_data["email"],
                role=user_data.get("role", "user"),
                profile_picture=user_data.get("profile_picture", ""),
            )
        return None

    # register page-controller blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(social_feed_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(bulletin_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)

    # make sure DB has the required tables
    # init_schema()
    return app


if __name__ == "__main__":
    app = create_app()
    # debug=True is only for local dev!
    app.run(debug=True)
