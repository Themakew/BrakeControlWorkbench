import serial


class ArduinoConnection:

    def __init__(self):
        self.arduino_port = '/dev/cu.wchusbserial1420'
        self.arduino_feedback = serial.Serial(self.arduino_port, 9600, timeout=10)

    def read_string_from_arduino(self):
        arduino_feedback_list = self.arduino_feedback.readline().split()
        return self.convert_list_to_dictionary(arduino_feedback_list)
