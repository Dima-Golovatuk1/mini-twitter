from flask import Flask
from .auth_routes import auth_bp
from .post_routes import post_bp
from .profile_routes import profile_bp
from .home_route import home_bp
from .other_routes import other_bp


def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/post')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(other_bp, url_prefix='/other')

    return app