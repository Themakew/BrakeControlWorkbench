from flask import Flask
from flask.ext.login import LoginManager
from mockdbhelper import MockDBHelper as DBHelper

app = Flask(__name__)
app.secret_key = "YqO29YjPwEWcV7w5UjzoamGL7+9UazD5MWcfM6ZgN/2lvQJtcjZHH2p+wSfZt\
7oNlW+7WQn80rvvS9C1CUWffFIHXz04qKSLkD9o"

login_manager = LoginManager(app)

DB = DBHelper()
