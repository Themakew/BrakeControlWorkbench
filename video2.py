# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

        imgGrayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # convert to grayscale
  
        imgBlurred = cv2.GaussianBlur(imgGrayscale, (5, 5), 0)          # blur
  
        imgCanny = cv2.Canny(imgBlurred, 100, 200)                      # get Canny edges

 
        cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)        # create windows, use WINDOW_AUTOSIZE for a fixed window size
        cv2.namedWindow("imgCanny", cv2.WINDOW_AUTOSIZE)           # or use WINDOW_NORMAL to allow window resizing

        cv2.imshow("image",image)         # show windows
        cv2.imshow("imgCanny", imgCanny)
  
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
      	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
	      	break
