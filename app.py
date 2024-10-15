from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from data.data_base.handlers import get_users_by_id, add_user_to_users, get_users, get_users_by_email

app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


# def get_post_by_id(post_id):
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     query = sql.SQL("SELECT post_name, content FROM posts WHERE id = %s")
#     cursor.execute(query, (post_id,))
#     post = cursor.fetchone()
#     cursor.close()
#     connection.close()

#     if post:
#         post_name, content = post
#         return {
#             'post_name': post_name,
#             'content': content
#         }
#     else:
#        return None

class User(UserMixin):
    def __init__(self, id, email, name, password, DOB, gender, rem=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.DOB = DOB
        self.gender = gender
        self.rem = rem

    def remember(self):
        return self.rem == 'on'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = get_users_by_id(user_id)
    if user:
        return User(id=user[0]['id'], email=user[0]['email'], name=user[0]['name'], password=user[0]['password'],
                    DOB=user[0]['birthday'], gender=user[0]['sex'],)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You need to be logged in to access this page.", "warning")
    return redirect(url_for('login'))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = get_users_by_email(email)
        rem = request.form.get('remember', 'off')
        list_users = get_users()
        if user and check_password_hash(s, password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('/'))
        else:
            return None

    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        DOB = request.form.get('dob')
        gender = request.form.get('gender')
        users_list = get_users()
        print(email)

        for user in users_list:
            if user["email"] == email:
                flash('Email is already registered.', 'danger')
                return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        hash_password = generate_password_hash(password)
        add_user_to_users(name, email, hash_password, DOB, gender)

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    if current_user.is_authenticated:
        name = current_user.name
        user_id = current_user.id
        posts = []
    else:
        name = None
        user_id = None
        posts = []

    return render_template('index.html', user_id=user_id, username=name, posts=posts)


@app.route('/explore')
@login_required
def explore():
    return render_template('explore.html')


@app.route('/messages',  methods=["GET", "POST"])
@login_required
def messages():
    if request.method == 'POST':


        return render_template('messages.html')


@app.route('/bookmarks')
@login_required
def bookmarks():
    return render_template('bookmarks.html')


@app.route('/profile')
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        DOB = request.form.get('dob')
        gender = request.form.get('gender')

    return render_template('profile.html')


@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')


@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post_data = get_post_by_id(post_id)
    if post_data:
        post_name = post_data['post_name']
        content = post_data['content']
        return render_template('post.html', post_name=post_name, content=content, post_id=post_id)
    else:
        return redirect(url_for('explore'))


if __name__ == '__main__':
    app.run(debug=True)
