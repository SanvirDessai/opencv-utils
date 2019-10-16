import numpy as np
import cv2

class MotionDetector ():

	""" Motion detection class """

	def __init__ (self, sensitivity, blur, objMinSize):

		self._sensitivity = sensitivity
		self._blur = blur
		self._objMinSize = objMinSize
		self._showDifference = False


	def detect (self, Frame1, Frame2):

		""" Returns an array of moving objects detected using background subtraction between Frame1 and Frame2 """

		gray1 = cv2.cvtColor(Frame1, cv2.COLOR_BGR2GRAY)
		gray2 = cv2.cvtColor(Frame2, cv2.COLOR_BGR2GRAY)
		differenceImage = cv2.absdiff(gray1, gray2)

		retval, thresholdImage = cv2.threshold(differenceImage, self._sensitivity, 255, cv2.THRESH_BINARY)
		blurred = cv2.blur(thresholdImage, (self._blur, self._blur))
		retval, processedThreshold = cv2.threshold(blurred, self._sensitivity, 255, cv2.THRESH_BINARY)
		image, contours, hierarchy = cv2.findContours(processedThreshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		if self._showDifference:
			cv2.imshow('diff', image)

		objects = []
		if len(contours) > 0:
			for contour in contours:
				boundingRect = cv2.boundingRect(contour)
				area = boundingRect[2] * boundingRect[3]

				if area > (self._objMinSize * self._objMinSize):
					objects.append(boundingRect)

		return objects

	def enableDifferenceImage (self):
		""" Enables the difference image video stream for manually calibrating the sleep period """
		self._showDifference = True

	def disableDifferenceImage (self):
		""" Disables the difference image video stream for manually calibrating the sleep period """
		self._showDifference = False