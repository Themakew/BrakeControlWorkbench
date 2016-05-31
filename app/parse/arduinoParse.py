import serial


class ArduinoConnection:

    def __init__(self):
        self.arduino_port = '/dev/cu.wchusbserial1420'
        self.arduino_feedback = serial.Serial(self.arduino_port, 9600, timeout=10)

    def read_string_from_arduino(self):
        while True:
            arduino_feedback_list = self.arduino_feedback.readline().split()
            return self.convert_list_to_dictionary(arduino_feedback_list)

    def convert_list_to_dictionary(self, arduino_feedback_list):
        arduino_feedback_dictionary = {"environment_tempeture": float(arduino_feedback_list[0]),
                                       "disc_temperature": float(arduino_feedback_list[1]),
                                       "pincers_temperature": float(arduino_feedback_list[2]),
                                       "engine_speed": float(arduino_feedback_list[3]),
                                       "disc_pressure": float(arduino_feedback_list[4]),
                                       "frictional_force": float(arduino_feedback_list[5])}
        # print arduino_feedback_dictionary
        return arduino_feedback_dictionary

if __name__ == '__main__':
    instance = ArduinoConnection()
    instance.read_string_from_arduino()
