from motion import MotionDetector
from stream import Stream
from fps import FPS
import time
import cv2

# enable optimised mode if possible
optimized = cv2.useOptimized()
if not optimized:
    cv2.setUseOptimized(True)

# initialise new motion detector
motionDetector = MotionDetector(20, 20, 200)
motionDetector.enableDifferenceImage()

# start new video capture and initialise new frames
capture = Stream(src=0).start()
ret, frame = capture.read()
ret2, frame2 = capture.read()

# initialise an array to store detected objects
objects = []

# start FPS recorder
fps = FPS().start()

while True:

    # get new detected objects
    objects = motionDetector.detect(frame, frame2)

    # get 1st frame and make a copy for display
    ret, frame = capture.read()
    display = frame.copy()

    # background subtraction works by obtaining the difference between two frames
    # when video is running on a separate thread as in this case,
    # there are no time consuming operations taking place between frame captures,
    # hence frame1 is very similar to frame2 and no difference is seen
    # thus a sleep is introduced to consume time between frame grabs
    # this can be replaced by any required computation
    time.sleep(0.02)

    # draw rectangle around each detected object
    for obj in objects:
        cv2.rectangle(display, (obj[0], obj[1]), (obj[2], obj[3]), (0,255, 0), 1)

    # display result
    cv2.imshow('Video', display)
    
    # get 2nd frame after some time has passed
    ret2, frame2 = capture.read()
    
    # update FPS data
    fps.update()

    # press q to exit loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# stop recording FPS data and log final values
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# release video stream and close any opened cv2 windows
capture.release()
cv2.destroyAllWindows()