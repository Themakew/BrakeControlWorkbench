import serial


class ArduinoConnection:

    def __init__(self):
        self.arduino_port = '/dev/cu.wchusbserial1420'
        self.arduino_feedback = serial.Serial(self.arduino_port, 9600, timeout=10)

    def read_string_from_arduino(self):
        while True:
            arduino_feedback_list = self.arduino_feedback.readline().split()
            self.convert_list_to_dictionary(arduino_feedback_list)

            # return arduino_feedback_dictionary

    def convert_list_to_dictionary(self, arduino_feedback_list):
        arduino_feedback_dictionary = {"var_one": float(arduino_feedback_list[0]),
                                       "var_two": float(arduino_feedback_list[1]),
                                       "var_three": float(arduino_feedback_list[2]),
                                       "var_four": float(arduino_feedback_list[3]),
                                       "var_five": float(arduino_feedback_list[4]),
                                       "var_six": float(arduino_feedback_list[5])}
        print arduino_feedback_dictionary
        # return arduino_feedback_dictionary

if __name__ == '__main__':
    instance = ArduinoConnection()
    instance.read_string_from_arduino()
