from flask import Flask
from presentation.controller.login_controller import login_bp
# from data_source.login_queries import init_schema

def create_app():
    app = Flask(__name__,
                template_folder="presentation/templates",
                static_folder="presentation/static",
                static_url_path="/static")
    app.config['SECRET_KEY'] = 'd9a8f7c6e5b4d3c2b1a0f9e8d7c6b5a4'

    # register page-controller blueprints
    app.register_blueprint(login_bp)

    # make sure DB has the required tables
    # init_schema()
    return app

if __name__ == "__main__":
    app = create_app()
    # debug=True is only for local dev!
    app.run(debug=True)
