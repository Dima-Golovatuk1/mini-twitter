from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from data.data_base.handlers import *


app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


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
    user = get_user_by_id(user_id)
    if user:
        return User(id=user['id'], email=user['email'], name=user['name'], password=user['password'],
                    DOB=user['birthday'], gender=user['sex'])
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You need to be logged in to access this page.", "warning")
    return redirect(url_for('login'))


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        rem = request.form.get('remember', 'off')
        user = get_users_by_email(email)

        if not user:
            flash("Email doesn't exist", "danger")
            return redirect(url_for('login'))

        user = user[0]

        if check_password_hash(user['password'], password):
            user_obj = User(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                password=user["password"],
                DOB=user["birthday"],
                gender=user["sex"],
                rem=rem
            )
            login_user(user_obj, remember=user_obj.remember())
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':

        def validate_email_format(email):
            try:
                valid = validate_email(email)
                return True
            except EmailNotValidError:
                return False

        email = request.form.get('email')
        name = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        DOB = request.form.get('dob')
        gender = request.form.get('gender')
        users_list = get_users()

        for user in users_list:
            if user['name'] == name:
                flash('Username is already registered', 'danger')
                return render_template('register.html')

            if user['email'] == email:
                flash('Email is already registered', 'danger')
                return render_template('register.html')

        if not validate_email_format(email):
            flash("Invalid email format", "danger")
            return render_template('register.html')

        if len(password) < 8:
            flash('Your password must have more than 8 characters', 'danger')
            return render_template('register.html')

        if not any(char.isalpha() for char in password):
            flash('Your password must contain at least one letter', 'danger')
            return render_template('register.html')

        if not any(char.isupper() for char in password):
            flash('Your password must contain at least one uppercase letter', 'danger')
            return render_template('register.html')

        if not any(char.islower() for char in password):
            flash('Your password must contain at least one lowercase letter', 'danger')
            return render_template('register.html')

        if not any(char.isdigit() for char in password):
            flash('Your password must contain at least one digit ', 'danger')
            return render_template('register.html')

        if any(char.isspace() for char in password):
            flash("Your password can't contain spaces", 'danger')
            return render_template('register.html')

        special_characters = '!@#$%^&*(),.?":{}|<>'
        special_characters_list = list(special_characters)
        if not any(special_characters_list for special_character in password):
            flash('Your password must contain at least one special character', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash("Passwords don't match", 'danger')
            return render_template('register.html')

        hash_password = generate_password_hash(password)
        add_user_to_users(name, email, hash_password, DOB, gender)

        flash('Registration successful! You can now log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/')
@login_required
def home():
    name = current_user.name
    user_id = current_user.id
    posts = []
    all_post = get_all_posts()
    return render_template('index.html', user_id=user_id, username=name, posts=posts, all_post=all_post)


@app.route('/explore', methods=['POST', 'GET'])
@login_required
def explore():
    all_posts = get_all_posts()

    if request.method == 'POST':
        title = request.form.get('explore_input').strip()
        posts_by_title = get_post_by_title_partial(title)

        if posts_by_title:
            return render_template('explore.html', all_post=posts_by_title, search=title)
        else:
            flash('No posts found for the search query.', 'danger')
            return render_template('explore.html', all_post=None, search=title)

    return render_template('explore.html', all_post=all_posts)


@app.route('/profile')
@login_required
def profile():
    name = current_user.name
    user_id = current_user.id
    email = current_user.email
    DOB = current_user.DOB
    gender = current_user.gender
    password = current_user.password
    posts = []
    all_user_posts = get_all_posts_by_user_id(user_id)
    return render_template('profile.html',
                           username=name, email=email, DOB=DOB, gender=gender, user_id=user_id,
                           posts=posts, all_post=all_user_posts)


@app.route('/view_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def view_profile(id):
    user = get_user_by_id(id)
    all_post = get_all_posts_by_user_id(id)
    user_id = current_user.id
    followers = get_followers_by_user_id(id)

    is_following = user_id in followers

    if request.method == 'POST':
        if is_following:
            remove_follower(user_id, id)
            is_following = False
        if not is_following:
            add_new_follower(user_id, id)
            is_following = True

    return render_template('view.html', name=user['name'],
                           id=id, birthday=user['birthday'], sex=user['sex'],
                           all_post=all_post, is_following=is_following)


@app.route('/global')
@login_required
def global_page():
    name = current_user.name
    user_id = current_user.id
    posts = []
    all_post = get_all_posts()
    return render_template('global.html', user_id=user_id, username=name, posts=posts, all_post=all_post)


@app.route('/following')
@login_required
def following():
    return render_template('following.html')


@app.route('/addpost', methods=["GET", "POST"])
@login_required
def addpost():
    user_id = current_user.id
    all_user_posts = get_all_posts_by_user_id(user_id)
    if request.method == 'POST':
        user_id = current_user.id
        title = request.form.get('title')
        content = request.form.get('content')
        post_img = request.files.get('post_img')
        post_video = request.form.get('post_video')

        if not title or not content:
            flash('Please fill out all required fields.', 'danger')
            return render_template('addpost.html')

        if post_img:
            image = post_img.filename
            image_path = f'static/downloaded_images/{image}'
            post_img.save(image_path)
        else:
            image_path = None

        create_new_post(user_id, title, content, image_path, post_video)
        flash('Post created successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('addpost.html', all_post=all_user_posts)


@app.route('/post/<int:id>', methods=('POST', 'GET'))
@login_required
def post(id):
    post_data = get_post_by_id(id)
    if not post_data:
        return redirect(url_for('explore'))

    title = post_data[0]['title']
    content = post_data[0]['content']
    comments = get_all_comments_by_post_id(id)

    if request.method == 'POST':
        user_id = current_user.id
        post_id = id
        comment = request.form.get('comment')
        if comment:
            add_comment(user_id, post_id, comment)
            return redirect(url_for('post', id=id))

    return render_template('post.html',
                           title=title, content=content, id=id, comments=comments)


@app.route('/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post():
    user_id = current_user.id
    all_user_posts = get_all_posts_by_user_id(user_id)

    if request.method == 'POST':
        post_title = request.form.get('delete_post')
        if post_title:
            post = get_post_by_title_and_user_id(post_title, user_id)
            if post:
                delete_post_by_id(post['id'])
                return redirect(url_for('delete_post'))
            else:
                flash("No post found with that title.", 'danger')
                return redirect(url_for('delete_post'))

    return render_template('delete_post.html', user_id=user_id, all_post=all_user_posts)


@app.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = get_comment_by_id(id)

    if not comment:
        flash("Comment not found.", "danger")
        return redirect(url_for("home"))

    post_id = comment[0]['post_id']
    post = get_post_by_id(post_id)

    if not post:
        flash("Post not found.", "danger")
        return redirect(url_for("home"))

    comment_owner = comment[0]['user_id']
    user_id = current_user.id

    if comment_owner != user_id:
        flash("You are not the owner of this comment to delete it.", "danger")
        return redirect(url_for("post", id=post_id))

    if request.method == 'POST':
        delete_comment_by_id(id)
        flash("Comment deleted successfully.", "success")
        return redirect(url_for("post", id=post_id))

    return render_template('delete_comment.html', comment=comment[0], post_id=post_id)


if __name__ == '__main__':
    app.run(debug=True)
