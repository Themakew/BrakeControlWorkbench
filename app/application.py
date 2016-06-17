from celery import Celery
from flask import Flask
from flask.ext.login import LoginManager
from mockdbhelper import MockDBHelper as DBHelper
from datetime import timedelta
from flask import app
from flask import session
from models import BrakeControl


app = Flask(__name__)
app.secret_key = "YqO29YjPwEWcV7w5UjzoamGL7+9UazD5MWcfM6ZgN/2lvQJtcjZHH2p+wSfZt\
7oNlW+7WQn80rvvS9C1CUWffFIHXz04qKSLkD9o"
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

login_manager = LoginManager(app)

DB = DBHelper()

bcontrol = BrakeControl()


@app.before_request
def make_session_permanent():
    bcontrol.stop_test()
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)# 1 minute just for test
