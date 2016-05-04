import picamera.array 
import time

import threading
import picamera
import cv2



class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
             
            # camera setup
            camera.resolution = (640, 480)
            camera.hflip = True
            camera.vflip = True
            camera.framerate = 32
            

            # let camera warm up
            time.sleep(0.1)
            with picamera.array.PiRGBArray(camera, size=(640, 480)) as stream:

                for foo in camera.capture_continuous(stream, format="bgr", use_video_port=True):
                # store frame
                
                    image = foo.array
                
                    imgGrayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)          # convert to grayscale
                    imgBlurred = cv2.GaussianBlur(imgGrayscale, (5, 5), 0)          # blur
                    imgCanny = cv2.Canny(imgBlurred, 100, 200)                      # get Canny edges

                    jpeg = cv2.imencode('.jpg', imgCanny)
                
                    cls.frame = jpeg

                # reset stream for next frame
                    stream.truncate(0)
                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                    if time.time() - cls.last_access > 10:
                        break
        cls.thread = None

