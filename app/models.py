import RPi.GPIO as GPIO
from celery.task.control import revoke
import time


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
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(29, GPIO.OUT)
        GPIO.setup(31, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        GPIO.setup(35, GPIO.OUT)
        self.motor = False
        self.brake = False
        self.taskID = None
        self.cycles = 0
        self.currentCycle = 0
        self.velMax = 0

    def turn_on_engine(self):
        self.motor = True
        self.brake = False
        GPIO.output(11, self.brake)
        time.sleep(0.5)
        GPIO.output(7, self.motor)

    def brake_engine(self):
        self.motor = False
        self.brake = True
        GPIO.output(7, self.motor)
        time.sleep(0.5)
        GPIO.output(11, self.brake)

    def turn_off_all(self):
        self.motor = False
        self.brake = False
        GPIO.output(11, self.brake)
        GPIO.output(7, self.motor)
        GPIO.output(29, False)
        GPIO.output(31, False)
        GPIO.output(33, False)
        GPIO.output(35, False)

    def stop_test(self):
        self.turn_off_all()

    def set_velMax(self, vel):
        self.velMax = vel
        self.setpins()

    def setpins(self):
        if self.velMax == "80 Km/h":
            self.sendPinSignal(True, True, False, True)
        elif self.velMax == "60 Km/h":
            self.sendPinSignal(True, False, False, False)
        elif self.velMax == "40 Km/h":
            self.sendPinSignal(False, True, True, True)

    def sendPinSignal(self, bit1, bit2, bit3, bit4):
        GPIO.output(29, bit1)
        GPIO.output(31, bit2)
        GPIO.output(33, bit3)
        GPIO.output(35, bit4)
