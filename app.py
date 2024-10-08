from flask import Flask, render_template, url_for, redirect
import flask_login


app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/explore')
def explore():
    render_template('index.html')


@app.route('/messages')
def messages():
    render_template('index.html')


@app.route('/bookmarks')
def bookmarks():
    render_template('index.html')


@app.route('/profile')
def profile():
    render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
