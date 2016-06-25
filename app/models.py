#import RPi.GPIO as GPIO
from celery.task.control import revoke


class User:
    def __init__(self, email):
        self.email = email

    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class BrakeControl(object):
    def __init__(self):
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(7, GPIO.OUT)
        #GPIO.setup(11, GPIO.OUT)
        self.motor = False
        self.brake = False
        self.taskID = None
        self.cycles = 0
        self.currentCycle = 0
        self.velMax = 0
        self.velMin = 0

    def turn_on_engine(self):
        self.motor = True
        self.brake = False
        self.send_signal()

    def brake_engine(self):
        self.motor = False
        self.brake = True
        self.send_signal()

    def turn_off_all(self):
        self.motor = False
        self.brake = False
        self.send_signal()

    def send_signal(self):
        #GPIO.output(7, self.motor)
        #GPIO.output(11, self.brake)
        pass

    def stop_test(self):
        self.turn_off_all()
        #revoke(self.taskID, terminate=True)
