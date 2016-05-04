from flask import Flask, render_template, Response
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import time



camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        image = frame.array
        yield (b'--image\r\n'
               b'Content-Type: imagee/jpeg\r\n\r\n' + image + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(PiCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=image')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
