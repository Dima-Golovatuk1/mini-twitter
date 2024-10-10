from flask import Flask, render_template, url_for, redirect
import flask_login


app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template('register.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/messages.html')
def messages():
    return render_template('messages.html')


@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/notifications')
def notifications():
    return render_template('notifications.html')


if __name__ == '__main__':
    app.run(debug=True)
