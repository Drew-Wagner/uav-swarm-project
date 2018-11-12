"""This file has mostly been replace by 'Glove Detection And Tracking'\gloveGestureTracking.py"""
import cv2
import numpy as np
import time


def Color(h, s, v):
	return np.array([h, s, v], dtype=np.uint8)


class ColorFinder:
	def __init__(self, name, lower, upper, trackbars=True):
		self.name = name
		self.lower = lower
		self.upper = upper
		if trackbars:
			cv2.namedWindow(name)
			cv2.createTrackbar("lower_h", name, self.lower[0], 255, self.update_lower_h)
			cv2.createTrackbar("upper_h", name, self.upper[0], 255, self.update_upper_h)
			cv2.createTrackbar("lower_s", name, self.lower[1], 255, self.update_lower_s)
			cv2.createTrackbar("upper_s", name, self.upper[1], 255, self.update_upper_s)
			cv2.createTrackbar("lower_v", name, self.lower[2], 255, self.update_lower_v)
			cv2.createTrackbar("upper_v", name, self.upper[2], 255, self.update_upper_v)

	def update_lower_h(self, val):
		self.lower[0] = val

	def update_upper_h(self, val):
		self.upper[0] = val

	def update_lower_s(self, val):
		self.lower[1] = val

	def update_upper_s(self, val):
		self.upper[1] = val

	def update_lower_v(self, val):
		self.lower[2] = val

	def update_upper_v(self, val):
		self.upper[2] = val

	def find_color(self, image, show=False):
		mask = cv2.inRange(image, self.lower, self.upper)
		if show:
			cv2.imshow("mask_" + self.name, mask)
		return mask

class HandTracker:
	def morph_open_close(self, mask):
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
		return mask


	def find_biggest_contours(self, mask):
		mask = self.morph_open_close(mask)
		cv2.imshow("mask", mask)

		_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		if contours:
			return sorted(contours, key=lambda contour: cv2.contourArea(contour), reverse=True)[0]
		else:
			return None

	def get_centroid_of_contour(self, contour):
		moments = cv2.moments(contour)
		centroid_x = 0
		centroid_y = 0
		if moments["m00"] > 0:
			centroid_x = moments["m01"]/moments["m00"]
			centroid_y = moments["m10"]/moments["m00"]
		return (centroid_x, centroid_y)

	def get_convex_hull_with_points(self, contour):
		return cv2.convexHull(contour, returnPoints=True)

	def get_all_convexity_defects(self, contour):
		hull_no_points = cv2.convexHull(contour, returnPoints=False)
		return cv2.convexityDefects(contour, hull_no_points)

	def get_resonable_convexity_defects(self, contour):
		all_defects = self.get_all_convexity_defects(contour)
		if all_defects is None:
			return []
		width, height = cv2.boundingRect(contour)[2:]
		length = max(width, height)

		good_defects = []
		for defect in all_defects:
			s,e,f,sqr_d = defect.ravel()
			d = sqr_d**0.5
			if d > 0.4*length:
				good_defects.append((s,e,f,d))
		return good_defects



	def track_hand(self, image, mask):
		hand_contour = self.find_biggest_contours(mask)
		if hand_contour is None:
			return

		good_defects = self.get_resonable_convexity_defects(hand_contour)
		for s,e,f,sqr_d in good_defects:
			cv2.circle(image, tuple(hand_contour[f][0]),3, (0,0,255), 2)
		cv2.drawContours(image, [hand_contour], -1, (255,0,0), 2)
		return self.get_centroid_of_contour(hand_contour)


clove_CDF = ColorFinder("purple", Color(164, 5, 21), Color(222, 255, 255))
hand_tracker = HandTracker()
cap = cv2.VideoCapture(1)
try:
	dt = 1 / 25
	while True:
		t = time.time()

		#### Code goes here
		ret, frame_bgr = cap.read()
		if not ret:
			print("End of stream")
			break

		frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV_FULL)
		mask = clove_CDF.find_color(frame_hsv)
		pos = hand_tracker.track_hand(frame_bgr, mask)
		cv2.putText(frame_bgr, str(pos), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
		cv2.imshow("BGR", frame_bgr)
		###################

		k = cv2.waitKey(30) & 0xff
		if k == 27:
			break

		dt = time.time() - t - 0.03
		FPS = 1 / dt
		print(FPS)

finally:
	cap.release()
	cv2.destroyAllWindows()
