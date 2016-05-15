from flask import Flask
from flask import render_template
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from mockdbhelper import MockDBHelper as DBHelper
from user import User
from flask import redirect
from flask import url_for
from flask import request

DB = DBHelper()


app = Flask(__name__)
app.secret_key = "YqO29YjPwEWcV7w5UjzoamGL7+9UazD5MWcfM6ZgN/2lvQJtcjZHH2p+wSfZt\
7oNlW+7WQn80rvvS9C1CUWffFIHXz04qKSLkD9o"
login_manager = LoginManager(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
@login_required
def control_painel():
    return "You are logged in"


@app.route("/", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        print email
        password = request.form["password"]
        user_password = DB.get_user(email)

        if user_password and user_password == password:
            user = User(email)
            login_user(user)
            return redirect(url_for("control_painel"))
        return control_painel()


@app.route("/home")
def logout():
   logout_user()
   return redirect(url_for("index"))


@login_manager.user_loader
def load_user(user_id):
   user_password = DB.get_user(user_id)
   if user_password:
      return User(user_id)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
