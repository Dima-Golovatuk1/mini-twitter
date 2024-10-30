from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from app.data.data_base import *


app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


def get_embed_url(video_url):
    if not video_url:
        return None

    if "tiktok.com" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        return f"https://www.tiktok.com/embed/{video_id}"

    if "youtube.com" in video_url:
        if "watch?v=" in video_url:
            video_url = video_url.replace("watch?v=", "embed/")
        elif "/shorts/" in video_url:
            video_id = video_url.split("/shorts/")[-1].split('?')[0]
            video_url = f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        video_url = f"https://www.youtube.com/embed/{video_id}"

    if "&" in video_url:
        video_url = video_url.split("&")[0]

    if "vimeo.com" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        video_url = f"https://player.vimeo.com/video/{video_id}"

    return video_url


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

    all_post = get_all_posts()

    for post in all_post:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    return render_template('index.html',
                           user_id=user_id, username=name, posts=all_post, all_post=all_post)


@app.route('/explore', methods=['POST', 'GET'])
@login_required
def explore():
    all_posts = get_all_posts()

    for post in all_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    if request.method == 'POST':
        title = request.form.get('explore_input').strip()
        posts_by_title = get_post_by_title_partial(title)

        for post in posts_by_title:
            if post.get('video_url'):
                post['video_url'] = get_embed_url(post['video_url'])

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

    for post in all_user_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    return render_template('profile.html',
                           username=name, email=email, DOB=DOB, gender=gender, user_id=user_id,
                           posts=posts, all_post=all_user_posts)


@app.route('/view_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def view_profile(id):
    user = get_user_by_id(id)
    all_posts = get_all_posts_by_user_id(id)
    user_id = current_user.id
    is_following_status = checking_if_user_is_follower(user_id, id)

    for post in all_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    if user:
        if request.method == 'POST':
            if is_following_status:
                remove_follower(user_id, id)
                flash('You have unfollowed this user.', 'success')
            else:
                add_new_follower(user_id, id)
                flash('You are now following this user.', 'success')

            return redirect(url_for('view_profile', id=id))

        return render_template('view.html', name=user['name'],
                               id=id, birthday=user['birthday'], sex=user['sex'],
                               all_post=all_posts, is_following=is_following_status,
                               idol=id, user_id=user_id)
    else:
        flash("That user doesn't exist", 'danger')
        return redirect(url_for('home'))


@app.route('/global')
@login_required
def global_page():
    name = current_user.name
    user_id = current_user.id
    posts = []
    all_post = get_all_posts()

    for post in all_post:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])
    return render_template('global.html', user_id=user_id, username=name, posts=posts, all_post=all_post)


@app.route('/following')
@login_required
def following():
    name = current_user.name
    user_id = current_user.id
    all_post = get_all_post_by_follower(user_id)

    for post in all_post:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    return render_template('following.html', user_id=user_id, username=name, posts=all_post)


@app.route('/addpost', methods=["GET", "POST"])
@login_required
def addpost():
    user_id = current_user.id
    all_user_posts = get_all_posts_by_user_id(user_id)
    for post in all_user_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post_img = request.files.get('post_img')
        post_video = request.form.get('post_video')

        if not title or not content:
            flash('Please fill out all required fields.', 'danger')
            return render_template('addpost.html')

        image_url = None

        if post_img:
            image = post_img.filename
            image_path = f'app/static/downloaded_images/{image}'
            post_img.save(image_path)
            image_url = url_for('static', filename=f'downloaded_images/{image}')

        create_new_post(user_id, title, content, image_url, post_video)
        flash('Post created successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('addpost.html', all_post=all_user_posts)


@app.route('/post/<int:id>', methods=('POST', 'GET'))
@login_required
def post(id):
    user_id = current_user.id
    post_data = get_post_by_id(id)
    if not post_data:
        return redirect(url_for('explore'))

    post_author_id = get_user_id_by_post_id(id)
    post_author = get_user_by_id(post_author_id)

    comment_author_id = get_all_author_id_by_comment()
    comment_author = get_users_by_list_id(comment_author_id)

    title = post_data[0]['title']
    content = post_data[0]['content']
    image_url = post_data[0].get('image_url')
    video_url = post_data[0].get('video_url')
    video_url = get_embed_url(video_url)
    comments = get_all_comments_by_post_id(id)
    user_id = current_user.id
    is_post_author = user_id == post_author_id

    for comment in comments:
        comment_author = get_user_by_id(comment['user_id'])
        comment['author_name'] = comment_author['name']
        comment['author_id'] = comment_author['id']

    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            add_comment(user_id, id, comment)
            flash('Your comment has been added!', 'success')
            return redirect(url_for('post', id=id))

    return render_template('post.html',
                           title=title, content=content, id=id, comments=comments,
                           post_author=post_author['name'], post_author_id=post_author_id,
                           image_url=image_url, video_url=video_url, user_id=user_id,
                           is_post_author=is_post_author, comment_author=comment_author)


@app.route('/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post():
    user_id = current_user.id
    all_user_posts = get_all_posts_by_user_id(user_id)
    for post in all_user_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    if request.method == 'POST':
        post_title = request.form.get('delete_post')
        if post_title:
            post = get_post_by_title_and_user_id(post_title, user_id)
            if post:
                delete_post_by_id(post['id'])
                flash("Post deleted succesfully", 'success')
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


@app.route('/all_users')
@login_required
def all_users():
    users = get_users()
    return render_template('all_users.html', users=users)


@app.route('/all_following_users')
@login_required
def all_following_users():
    user_id = current_user.id
    following_ids = get_following_by_user_id(user_id)

    following_users = get_users_by_list_id(following_ids)

    if following_users:
        return render_template('all_following_users.html', users=following_users)
    else:
        flash("You haven't any follows", 'danger')
        return redirect(url_for('all_users'))


if __name__ == '__main__':
    app.run(debug=True)