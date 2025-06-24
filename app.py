import profile
from flask import Flask
from presentation.controller.login_controller import login_bp
from presentation.controller.social_feed_controller import social_feed_bp
from presentation.controller.register_controller import register_bp
from presentation.controller.bulletin_controller import bulletin_bp
from presentation.controller.profile_controller import profile_bp
# from data_source.login_queries import init_schema

def create_app():
    app = Flask(__name__,
                template_folder="presentation/templates",
                static_folder="presentation/static",
                static_url_path="/static")
    
    app.secret_key = 'd9a8f7c6e5b4d3c2b1a0f9e8d7c6b5a4'

    # register page-controller blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(social_feed_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(bulletin_bp)
    app.register_blueprint(profile_bp)


    # make sure DB has the required tables
    # init_schema()
    return app

if __name__ == "__main__":
    app = create_app()
    # debug=True is only for local dev!
    app.run(debug=True)
