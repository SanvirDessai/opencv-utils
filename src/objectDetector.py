import cv2

DETECTION_MODELS = {
    'EYE': 'haarcascades/haarcascade_eye.xml',
    'FRONTAL_FACE': 'haarcascades/haarcascade_frontalface_default.xml',
    'PROFILE_FACE': 'haarcascades/haarcascade_profileface_default.xml',
    'FULL_BODY': 'haarcascades/haarcascade_fullbody.xml',
    'UPPER_BODY': 'haarcascades/haarcascade_upperbody.xml',
    'LOWER_BODY': 'haarcascades/haarcascade_lowerbody.xml'
}

class ObjectDetector ():

    """
    Object detection class
    model = FRONTAL_FACE, PROFILE_FACE, EYE, FULL_BODY, UPPER_BODY, LOWER_BODY
    custom models can be built using the method described here https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html
    """

    def __init__ (self, model, minSize):
        
        """ model = FRONTAL_FACE, PROFILE_FACE, EYE, FULL_BODY, UPPER_BODY, LOWER_BODY """

        # Create object cascade classifier
        self._model = DETECTION_MODELS[model]
        self._cascade = cv2.CascadeClassifier(self._model)
        self._minSize = minSize

    def detect (self, Frame):
        
        """ returns an array of bounding boxes around the objects detected in the frame """

        rgb = Frame[:, :, ::-1]
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        # scaleFactor, minNeighbors and minSize should be tuned depending on use case
        # the values chosen here were for detecting frontal face profiles at relatively near distances
        objects = self._cascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(self._minSize, self._minSize),
			flags=cv2.CASCADE_SCALE_IMAGE
		)
        
        return objects