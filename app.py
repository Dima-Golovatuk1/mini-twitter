from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


users = []

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, email, name, password, DOB, gender):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.DOB = DOB
        self.gender = gender

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_by_email(email):
        for user in users:
            if user.email == email:
                return user
        return None


@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You need to be logged in to access this page.", "warning")
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_by_email(email)

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        DOB = request.form.get('DOB')
        gender = request.form.get('gender')

        if User.get_by_email(email):
            flash('Email is already registered', 'danger')
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            user_id = len(users) + 1
            new_user = User(user_id, email, name, hashed_password, DOB, gender)
            users.append(new_user)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')


@app.route('/bookmarks')
@login_required
def bookmarks():
    return render_template('bookmarks.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')


if __name__ == '__main__':
    app.run(debug=True)