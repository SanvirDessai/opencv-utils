from tracker import ObjectTracker
from stream import Stream
from fps import FPS
import cv2

# enable optimised mode if possible
optimized = cv2.useOptimized()
if not optimized:
    cv2.setUseOptimized(True)

# start new video capture
capture = Stream(src=0).start()
ret, frame = capture.read()

# select an object to track
bbox = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
obj = ObjectTracker(frame, bbox, 'KCF')

fps = FPS().start()

while True:
    # Read a new frame
    ret, frame = capture.read()

    # Update tracker
    obj.update(frame)

    # Draw bounding box
    cv2.rectangle(frame,
        (int(obj._bbox[0]), int(obj._bbox[1])), # x
        (int(obj._bbox[0] + obj._bbox[2]), int(obj._bbox[1] + obj._bbox[3])), # y
        (0,255,0), 1)

    # Display result
    cv2.imshow("Video", frame)

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