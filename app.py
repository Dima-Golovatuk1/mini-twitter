from flask import Flask, render_template, url_for, redirect
import flask_login


app = Flask(__name__)
app.secret_key = '-^c^e%1q4n%rc^fr6k5u$6#&_4e801ctf3%sro=_xycfcu5%qul'


@app.route('/')
def home():
    render_template('index.html')


@app.route('/')
def explore():
    render_template('index.html')


@app.route('/')
def messages():
    render_template('index.html')


@app.route('/')
def bookmarks():
    render_template('index.html')


@app.route('/')
def profile():
    render_template('index.html')

<<<<<<< HEAD

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> 23f391d7caebc00a44656f2396ea57f915e1e021
=======
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 491090f7eedfdbc15226440c69cd9dccc66799b9
