from flask import Flask, render_template, url_for, redirect
import flask_login


app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


@app.route('/')
def Home():
    return render_template('index.html')


@app.route('/Explore')
def Explore():
    return render_template('index.html')


@app.route('/Messages')
def Messages():
    return render_template('index.html')


@app.route('/Bookmarks')
def Bookmarks():
    return render_template('index.html')


@app.route('/Profile')
def Profile():
def home():
    return render_template('index.html')


@app.route('/explore')
def explore():
    return render_template('index.html')


@app.route('/messages')
def messages():
    return render_template('index.html')


@app.route('/bookmarks')
def bookmarks():
    return render_template('index.html')


@app.route('/profile')
def profile():


if __name__ == '__main__':
    app.run(debug=True)
