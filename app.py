from flask import Flask

from presentation.controller.login_controller import login_bp
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

    # register page-controller blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(social_feed_bp)
    app.register_blueprint(register_bp)

    # make sure DB has the required tables
    # init_schema()
    return app


if __name__ == "__main__":
    app = create_app()
    # debug=True is only for local dev!
    app.run(debug=True)
