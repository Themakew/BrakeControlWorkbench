import serial

# Specific port in computer tha the arduino is connected
port = '/dev/cu.wchusbserial1420'

# String from arduino
arduinoFeedback = serial.Serial(port, 9600, timeout=10)

while True:
    print arduinoFeedback.readline()
