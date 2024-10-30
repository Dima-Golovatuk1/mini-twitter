from flask import Flask
from flask_login import LoginManager
from routes.auth_routes import auth_bp
from routes.post_routes import post_bp
from routes.profile_routes import profile_bp
from routes.other_routes import other_bp
from routes.home_route import home_bp
from modules import login_manager

app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'
login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(other_bp)
app.register_blueprint(home_bp)

if __name__ == '__main__':
    app.run(debug=True)