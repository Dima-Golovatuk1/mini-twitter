from flask import Flask, render_template, url_for, redirect
import flask_login


app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


@app.route('/')
def Home():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template('register.html')


@app.route('/Explore')
def Explore():
    return render_template('explore.html')


@app.route('/Messages.html')
def Messages():
    return render_template('messages.html')


@app.route('/Bookmarks')
def Bookmarks():
    return render_template('bookmarks.html')


@app.route('/Profile')
def Profile():
    return render_template('profile.html')


@app.route('/Notifications')
def Notifications():
    return render_template('notifications.html')


if __name__ == '__main__':
    app.run(debug=True)
