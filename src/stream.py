from threading import Thread
import cv2

class Stream:

	def __init__ (self, src):

		self._stream = cv2.VideoCapture(src)
		(self._ok, self._frame) = self._stream.read()

		self._stopped = False

	def start (self):

		Thread(target=self.capture, args=()).start()
		return self

	def capture (self):

		while True:
			if self._stopped:
				return

			(self._ok, self._frame) = self._stream.read()

	def read (self):
		return (self._ok, self._frame)

	def release (self):
		self._stopped = True
		self._stream.release()