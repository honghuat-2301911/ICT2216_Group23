from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from domain.entity.user import User
from data_source.user_queries import get_user_by_id

from presentation.controller.login_controller import login_bp
from presentation.controller.register_controller import register_bp
from presentation.controller.social_feed_controller import social_feed_bp

from presentation.controller.register_controller import register_bp
from presentation.controller.bulletin_controller import bulletin_bp
from presentation.controller.admin_controller import admin_bp
# from data_source.login_queries import init_schema


def create_app():
    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
        static_url_path="/static",
    )
    app.config['SECRET_KEY'] = 'ICT2216_Group23'
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_data = get_user_by_id(user_id)
        if user_data:
            return User(
                id=user_data["id"],
                name=user_data["name"],
                password=user_data["password"],
                email=user_data["email"],
                skill_lvl=user_data.get("skill_lvl"),
                sports_exp=user_data.get("sports_exp"),
                role=user_data.get("role", "user"),
            )
        return None

    # register page-controller blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(social_feed_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(bulletin_bp)
    app.register_blueprint(admin_bp)

    # make sure DB has the required tables
    # init_schema()
    return app


if __name__ == "__main__":
    app = create_app()
    # debug=True is only for local dev!
    app.run(debug=True)
