from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user

from app import app
from app import DB
from models import User
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
@login_required
def control_painel():
    return render_template("home.html")


@app.route("/", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_password = DB.get_user(email)

        if user_password and user_password == password:
            user = User(email)
            login_user(user)
            return control_painel() and redirect(url_for("control_painel"))
        return "User not logged!"


@app.route("/logout")
def logout():
    logout_user()
    return index() and redirect(url_for("index"))
