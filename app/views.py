from parse.arduinoParse import ArduinoConnection
from application import app
from application import celery
from application import DB
from application import login_manager
from application import bcontrol
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
import random

logged_user = False

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
    global logged_user
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_password = DB.get_user(email)

        if user_password and user_password == password:
            user = User(email)
            login_user(user)
            if logged_user == False:
                logged_user = True
                print "&&&&&&&&&& logged_user = {} *******".format(logged_user)
                return control_painel() and redirect(url_for("control_painel"))
            else:
                print "&&&&&&&&&&&&& Oooopssss &&&&&&&&&&&&&&&"
                return "Sorry, there is someone else using the bench"

        return "User not logged!"


@app.route("/logout")
def logout():
    global logged_user
    logout_user()
    logged_user = False
    print "&&&&&&&&&&&&&&&&&&& logged_user = {} *******".format(logged_user)
    return index() and redirect(url_for("index"))


@app.route("/brake", methods=['POST'])
def brake():
    brake_task.delay()
    return "Breaking engine response"


@app.route('/stop_test', methods=['POST'])
def stoptest():
    bcontrol.stop_test()
    return "Test Stopped by the server"


@app.route("/update_control_painel", methods=["POST"])
def update_control_painel():
    bcontrol.turn_on_engine()
    bcontrol.velMax = request.form['velocityMax']
    bcontrol.velMin = request.form['velocityMin']
    bcontrol.cycles = request.form['cycles']

    # task = read_string_from_arduino_continually.delay()
    task = read_string_mock.delay()
    bcontrol.taskID = task.id
    return jsonify({}), 202, {'Location': url_for('task_status', task_id=task.id)}


@app.route("/inittask/<task_id>")
def task_status(task_id):
    # task = read_string_from_arduino_continually.AsyncResult(task_id)
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


@celery.task
def brake_task():
    task = read_string_mock.AsyncResult(bcontrol.taskID)

    bcontrol.brake_engine()
    bcontrol.currentCycle += 1
    while True:
        if bcontrol.currentCycle == bcontrol.cycles:
            bcontrol.currentCycle = 0
            while int(task.info.get('speed')) > 0:
                continue

            bcontrol.stop_test()
            break
        else:
            if int(task.info.get('speed')) <= 40:
                bcontrol.turn_on_engine()
                break


def vel_mock(vel):
    if vel < bcontrol.velMax and bcontrol.motor:
        vel += 5
    elif vel > bcontrol.velMin and bcontrol.brake:
        vel -= 10

    return vel


@celery.task(bind=True)
def read_string_mock(self):
    speed = 0
    for i in range(120):
        dtemp = random.randint(30, 80)
        ptemp = random.randint(30, 70)
        etemp = random.randint(20, 35)
        press = random.randint(0, 100)
        frict = random.randint(0, 60)
        speed = vel_mock(speed)

        self.update_state(state='PROGRESS',
                          meta={'env_temp': etemp,
                                'pin_temp': ptemp,
                                'dsc_temp': dtemp,
                                'speed': speed,
                                'pressure': press,
                                'friction': frict
                                })
        time.sleep(0.5)

    return {'result': 0}


@celery.task(bind=True)
def read_string_from_arduino_continually(self):
    arduino_connection = ArduinoConnection()
    list_from_arduino = arduino_connection.read_string_from_arduino()

    while True:
        environment_tempeture = list_from_arduino[0]
        disc_temperature = list_from_arduino[1]
        pincers_temperature = list_from_arduino[2]
        engine_speed = list_from_arduino[3]
        disc_pressure = list_from_arduino[4]
        frictional_force = list_from_arduino[5]

        self.update_state(state='PROGRESS',
                          meta={'env_temp': environment_tempeture,
                                'pin_temp': pincers_temperature,
                                'dsc_temp': disc_temperature,
                                'speed': engine_speed,
                                'pressure': disc_pressure,
                                'friction': frictional_force
                                })
        time.sleep(0.5)

    return {'result': 1}


@app.route("/stop_test")
@login_required
def stop_test():
    print "stopped test"
    return redirect('/home')
