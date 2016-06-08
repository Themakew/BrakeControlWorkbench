from parse.arduinoParse import ArduinoConnection
from application import app
from application import celery
from application import DB
from application import login_manager
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from models import User
import time


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


@app.route("/update_control_painel", methods=["POST"])
def update_control_painel():
    task = read_string_from_arduino_continually.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@app.route("/start_test", methods=['POST'])
@login_required
def start_test():
    velocity = request.form['velocity']
    print("The velocity is '" + velocity + "'")
    return redirect('/home')


@app.route("/stop_test")
@login_required
def stop_test():
    print "stopped test"
    return redirect('/home')


@celery.task(bind=True)
def read_string_from_arduino_continually(self):
    self.environment_tempeture = 0.0
    self.disc_temperature = 0.0
    self.pincers_temperature = 0.0
    self.engine_speed = 0.0
    self.disc_pressure = 0.0
    self.frictional_force = 0.0

    self.arduino_connection = ArduinoConnection()
    self.dictionary = self.arduino_connection.read_string_from_arduino()

    i = 0
    while i < 5:
        self.update_state(state="FEEDBACK",
                          meta={"environment_tempeture": self.environment_tempeture,
                                "disc_temperature": self.disc_temperature,
                                "pincers_temperature": self.pincers_temperature,
                                "engine_speed": self.engine_speed,
                                "disc_pressure": self.disc_pressure,
                                "frictional_force": self.frictional_force})
        time.sleep(0.5)
    return {"environment_tempeture": 0.0,
            "disc_temperature": 0.0,
            "pincers_temperature": 0.0,
            "engine_speed": 0.0,
            "disc_pressure": 0.0,
            "frictional_force": 0.0}
