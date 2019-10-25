from objectDetector import ObjectDetector
from stream import Stream
from fps import FPS
import cv2

# enable optimised mode if possible
optimized = cv2.useOptimized()
if not optimized:
    cv2.setUseOptimized(True)

# initialise new frontal face detector
faceDetector = ObjectDetector(model='FRONTAL_FACE', minSize=35)

# start new video capture
capture = Stream(src=0).start()

# initialise an array to store detected objects
objects = []

# start FPS recorder
fps = FPS().start()

while True:

    ret, frame = capture.read()

    # optional resize to reduce computation
    # frame = cv2.resize(frame, (0, 0), fx=0.35, fy=0.35)

    # get new detected objects
    objects = faceDetector.detect(frame)

    # draw rectangle around each detected object
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255, 0), 1)

    # display result
    cv2.imshow('Video', frame)
    
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