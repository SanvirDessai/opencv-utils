import cv2

trackerTypes = {
	'BOOSTING': cv2.TrackerBoosting_create(),
	'MIL': cv2.TrackerMIL_create(),
	'KCF': cv2.TrackerKCF_create(),
	'TLD': cv2.TrackerTLD_create(),
	'MEDIANFLOW': cv2.TrackerMedianFlow_create()
}

class ObjectTracker ():
	def __init__ (self, Frame, Bbox, Tracker):
		""" Initialise the tracker using the bounding box of the object in the frame """
		
		# create tracker
        # KCF is the default
		tracker = cv2.TrackerKCF_create()
		
		if Tracker is 'BOOSTING': 
			tracker = cv2.TrackerBoosting_create()
		elif Tracker is 'MIL': 
			tracker = cv2.TrackerMIL_create()
		elif Tracker is 'TLD':
			tracker = cv2.TrackerTLD_create()
		elif Tracker is 'MEDIANFLOW':
			tracker = cv2.TrackerMedianFlow_create()
		
        # initialise the tracker with the source frame
		ok = tracker.init(Frame, Bbox)

		if not ok:
			print("INFO: Object: Failed to initialise object tracker")

		self._bbox = Bbox
		self._tracker = tracker

	def update (self, Frame):
		""" Attempts to find and update object in frame 
            Store new location if found
        """

		# Try to find object in frame and update object if success
		success, bbox = self._tracker.update(Frame)
		if success:
			self._bbox = bbox