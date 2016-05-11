from flask import Flask
from flask import render_template
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from mockdbhelper import MockDBHelper as DBHelper
from user import User
from flask import redirect
from flask import url_for

DB = DBHelper()


app = Flask(__name__)
app.secret_key = "YqO29YjPwEWcV7w5UjzoamGL7+9UazD5MWcfM6ZgN/2lvQJtcjZHH2p+wSfZt\
7oNlW+7WQn80rvvS9C1CUWffFIHXz04qKSLkD9o"
login_manager = LoginManager(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/account")
@login_required
def account():
    return "You are logged in"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
