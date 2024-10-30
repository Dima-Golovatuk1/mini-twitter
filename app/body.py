from flask import Flask
from flask_login import LoginManager
from modules import load_user
from routes import configure_routes


def run_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    configure_routes(app)
    return app


if __name__ == '__main__':
    app = run_app()
    app.run(debug=True)
