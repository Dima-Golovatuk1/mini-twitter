<<<<<<< Updated upstream
from flask import Flask, render_template, url_for, redirect
import flask_login

=======
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.handlers import *
from email_validator import validate_email, EmailNotValidError
>>>>>>> Stashed changes

app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/messages')
def messages():
    return render_template('index.html')


@app.route('/bookmarks')
def bookmarks():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('index.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/messages')
def messages():
    return render_template('messages.html')


@app.route('/notifications')
def notifications():
    return render_template('notifications.html')


<<<<<<< Updated upstream
=======
@app.route('/global')
@login_required
def global_page():
    data = get_all_posts()
    return render_template('global.html', data=data)


@app.route('/following')
@login_required
def following():
    return render_template('following.html')


@app.route('/addpost', methods=["GET", "POST"])
@login_required
def addpost():
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

    return render_template('addpost.html')


@app.route('/post/<int:id>', methods=('POST', 'GET'))
@login_required
def post(id):
    post_data = get_post_by_id(id)
    if not post_data:
        return redirect(url_for('explore'))

    title = post_data[0]['title']
    content = post_data[0]['content']
    comments = get_all_comments_by_post_id(post_id=id)

    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            add_comment(id, comment)
            return redirect(url_for('post', id=id))

    return render_template('post.html',
                           title=title, content=content, id=id, comments=comments)


@app.route('/delete_post')
@login_required
def delete_post():
    pass


>>>>>>> Stashed changes
if __name__ == '__main__':
    app.run(debug=True)
