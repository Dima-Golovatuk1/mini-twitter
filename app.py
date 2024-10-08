from flask import Flask, render_template, url_for, redirect
import flask_login


app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


@app.route('/')
@login_required
def Home():
    return render_template('index.html')


@app.route('/Explore')
def Explore():
    return render_template('index.html')


@app.route('/Messages')
@login_required
def Messages():
    return render_template('index.html')


@app.route('/Bookmarks')
@login_required
def Bookmarks():
    return render_template('index.html')


@app.route('/Profile')
@login_required
def Profile():
    return render_template('index.html')


@app.route('/Notifications')
@login_required
def Notifications():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
