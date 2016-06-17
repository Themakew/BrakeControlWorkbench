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
    save_file_with_text()
    return render_template("index.html")


def save_file_with_text():
    results = []

    for x in [1, 2, 3]:
        results.append("Valor x")
        results.append("Valor y")

    with open("test.txt", "w") as f:
        for value in results:
            f.write(value)
            f.write("\n")


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
    # task = read_string_from_arduino_continually.apply_async()
    task = read_string_mock.delay()
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@app.route("/inittask/<task_id>")
def taskstatus(task_id):
    task = read_string_mock.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'env_temp': 0,
            'pin_temp': 0,
            'dsc_temp': 0,
            'speed': 0,
            'pressure': 0,
            'friction': 0
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'env_temp': task.info.get('env_temp'),
            'pin_temp': task.info.get('pin_temp'),
            'dsc_temp': task.info.get('dsc_temp'),
            'speed': task.info.get('speed'),
            'pressure': task.info.get('pressure'),
            'friction': task.info.get('friction')
        }
    else:
        response = {'state': 'ERROR....'}

    return jsonify(response)

# simple mock
import random
@celery.task(bind=True)
def read_string_mock(self):
    for i in range(120):
        dtemp = random.randint(30, 80)
        ptemp = random.randint(30, 70)
        etemp = random.randint(20, 35)
        speed = random.randint(40, 60)
        press = random.randint(0, 100)
        frict = random.randint(0, 60)

        self.update_state(state='PROGRESS',
                          meta={'env_temp': etemp,
                                'pin_temp': ptemp,
                                'dsc_temp': dtemp,
                                'speed': speed,
                                'pressure': press,
                                'friction': frict
                                })
        time.sleep(0.5)

    return {'result': 51}


@app.route("/start_test", methods=['POST'])
@login_required
def start_test():
    velocity = request.form['velocity']
    # print("The velocity is '" + velocity + "'")
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
