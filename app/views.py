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
import memcache


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/")
def index():
    return render_template("index.html")


def save_file_with_text():
    results = []

    for x in [1, 2, 3]:
        results.append("Valorx")
        results.append(" ")
        results.append("Valory")
        results.append("\n")

    with open("test.txt", "w") as f:
        for value in results:
            f.write(value)


def read_text_file():
    results = []

    with open('test.txt', 'r') as f:
        data = f.readlines()
        for line in data:
            words = line.split()
            results.append(words)

    print results


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


@app.route("/brake", methods=['POST'])
def brake():
    #task = brake_task.delay()
    bcontrol.brake_engine()
    return "Breaking engine response"


@app.route('/stop_test', methods=['POST'])
def stoptest():
    client = memcache.Client([('127.0.0.1', 11211)])
    client.set("isTesting", False)
    print "***************** isTesting was set to False **************"
    bcontrol.stop_test()
    return "Test Stopped by the server"

@app.route("/update_control_painel", methods=["POST"])
def update_control_painel():
    bcontrol.turn_on_engine()
    velMax = request.form['velocityMax']
    bcontrol.set_velMax(velMax)
    bcontrol.velMin = request.form['velocityMin']
    bcontrol.cycles = request.form['cycles']
    client = memcache.Client([('127.0.0.1', 11211)])
    client.set("isTesting", True)
    print "***************** isTesting was set to True **************"

    task = read_string_from_arduino_continually.delay()
    print "***************** Task should be running ***********************"
    return jsonify({}), 202, {'Location': url_for('task_status', task_id=task.id)}
    #return "Accelerate"


@app.route("/inittask/<task_id>")
def task_status(task_id):
    task = read_string_from_arduino_continually.AsyncResult(task_id)
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
    task = read_string_from_arduino_continually.AsyncResult(bcontrol.taskID)

    bcontrol.brake_engine()
    bcontrol.currentCycle += 1
    while bcontrol.isTesting:
        if bcontrol.currentCycle == bcontrol.cycles:
            bcontrol.currentCycle = 0
            while int(task.info.get('speed')) > 0:
                continue

            bcontrol.stop_test()
            break
        else:
            #if int(task.info.get('speed')) <= 40:
            #    bcontrol.turn_on_engine()
            #    break
            time.sleep(3)
            bcontrol.turn_on_engine()

    
@celery.task(bind=True)
def read_string_from_arduino_continually(self):
    arduino_connection = ArduinoConnection()
    client = memcache.Client([('127.0.0.1', 11211)])
    listaDados = []

    print "************* New task read_string_from_arduino created *************"
    while client.get("isTesting") == True:
        list_from_arduino = arduino_connection.read_string_from_arduino()

        #list_from_arduino = arduino_connection.read_string_mock()
        print list_from_arduino
        while len(list_from_arduino) < 6:
            print "List size less than 6"
            list_from_arduino = arduino_connection.read_string_from_arduino()

        listaDados.append(list_from_arduino)

        disc_temperature = list_from_arduino[0]
        environment_temperature = list_from_arduino[1]
        pincers_temperature = list_from_arduino[2]
        engine_speed = list_from_arduino[3]
        disc_pressure = list_from_arduino[4]
        frictional_force = list_from_arduino[5]

        self.update_state(state='PROGRESS',
                          meta={'env_temp': environment_temperature,
                                'pin_temp': pincers_temperature,
                                'dsc_temp': disc_temperature,
                                'speed': engine_speed,
                                'pressure': disc_pressure,
                                'friction': frictional_force
                                })
        time.sleep(0.2)

    with open("test.txt", "w") as f:
        for value in listaDados:
            f.write(value)

    print "************* Task read_string_from_arduino is DEAD *****************"
    return {'result': 51}

