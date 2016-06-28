import serial
import random


class ArduinoConnection:

    def __init__(self):
        #pass
        # self.arduino_port = '/dev/cu.wchusbserial1420'
        self.arduino_port = '/dev/ttyUSB0'
        self.arduino_feedback = serial.Serial(self.arduino_port, 9600, timeout=0.2)

    def read_string_from_arduino(self):
        try:
            flist = map(float, self.arduino_feedback.readline().split())
        except ValueError:
            flist = []
        return flist

    def read_string_mock(self):
        dtemp = random.randint(30, 800)
        ptemp = random.randint(30, 700)
        etemp = random.randint(20, 35)
        press = random.randint(0, 10000)
        frict = random.randint(0, 60)
        speed = random.randint(0, 80)

        l = [dtemp, ptemp, etemp, press, frict, speed]
        return l

