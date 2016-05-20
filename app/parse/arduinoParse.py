import serial


class ArduinoConnection:

    variable_one = " "
    variable_two = " "
    variable_three = " "
    variable_four = " "
    variable_five = " "
    variable_six = " "

    def read_string_from_arduino(self):
        # Specific port in computer tha the arduino is connected
        arduino_port = '/dev/cu.wchusbserial1420'

        # String from arduino
        arduino_feedback = serial.Serial(port, 9600, timeout = 10)

        while True
            arduino_feedback_list = arduinoFeedback.readline().split()
            variable_one = arduino_feedback_list[0]
            variable_two = arduino_feedback_list[1]
            variable_three = arduino_feedback_list[2]
            variable_four = arduino_feedback_list[3]
            variable_five = arduino_feedback_list[4]
            variable_six = arduino_feedback_list[5]


if __name__ == '__main__':
    instance = ArduinoConnection()
    instance.read_string_from_arduino()
