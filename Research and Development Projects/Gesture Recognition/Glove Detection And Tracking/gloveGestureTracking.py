import cv2
import numpy as np
import time


def hsv_color(h, s, v):
	"""
	Creates an HSV color as an numpy array.

	:param h: A hue as an integer between 0 and 255
	:param s: A saturation as an integer between 0 and 255
	:param v: A value as an integer between 0 and 255
	:return: np.array shape=(3,) dtype=np.uint8
	"""
	return np.array([h, s, v], dtype=np.uint8)


def cartesian_to_radial(point, center):
	"""
	Converts a cartesian position vector to a radial position vector about the defined center.

	:param point: np.array
	:param center: np.array
	:return: np.array
	"""
	v = point - center
	r = np.linalg.norm(v)
	theta = np.arctan2(v[0][1], v[0][0])
	return r, theta


def get_distance_between_points(point1, point2):
	"""
	Returns the distance between two points
	:param point1: np.array
	:param point2: np.array
	:return: float
	"""
	return np.linalg.norm(point1 - point2)


class ColorFinder:
	"""
	Finds a mask of all pixels in a specified HSV range in an image.
	"""

	def __init__(self, name, lower, upper, trackbars=False):
		"""
		:param name: string, The name of the color to be detected (Used only for labeling)
		:param lower: np.array, inital lower HSV bound
		:param upper: np.array, inital upper HSV bound
		:param trackbars: boolean, Whether or not to create a window for the trackbars
		"""
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
		"""
		Updates the lower hue bound.
		:param val: integer between 0-255
		:return:
		"""
		self.lower[0] = val

	def update_upper_h(self, val):
		"""
		Updates the upper hue bound.
		:param val: integer between 0-255
		:return:
		"""
		self.upper[0] = val

	def update_lower_s(self, val):
		"""
		Updates the lower saturation bound.
		:param val: integer between 0-255
		:return:
		"""
		self.lower[1] = val

	def update_upper_s(self, val):
		"""
		Updates the upper saturation bound.
		:param val: integer between 0-255
		:return:
		"""
		self.upper[1] = val

	def update_lower_v(self, val):
		"""
		Updates the lower value bound.
		:param val: integer between 0-255
		:return:
		"""
		self.lower[2] = val

	def update_upper_v(self, val):
		"""
		Updates the upper value bound.
		:param val: integer between 0-255
		:return:
		"""
		self.upper[2] = val

	@staticmethod
	def clean_mask(mask):
		"""
		Cleans up the mask using OpenCV's morphological operations.

		:param mask: np.array
		:return: np.array
		"""
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
		# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)))
		return mask

	def find_color(self, image, show=False):
		"""
		Returns a mask of all pixels in the specified HSV range.

		:param image:
		:param show: Where or not to show the mask
		:return:
		"""
		image = cv2.GaussianBlur(image, (7, 7), 0)

		mask = cv2.inRange(image, self.lower, self.upper)
		mask = self.clean_mask(mask)
		if show:
			cv2.imshow("mask_" + self.name, mask)

		return mask


class HandDetector:
	"""
	A class containing methods for detecting a hand, fingertips, and gestures.
	"""

	@staticmethod
	def get_hand_center(hand_contour):
		"""
		Returns the centroid of the hand contour.

		:param hand_contour: np.array
		:return: np.array, (x, y) coordinates of the hand's centroid
		"""
		cx = -1
		cy = -1
		moments = cv2.moments(hand_contour)
		if moments['m00'] > 0:
			cx = moments['m10'] / moments['m00']
			cy = moments['m01'] / moments['m00']
		return np.array([cx, cy])

	@staticmethod
	def get_hand_ellipse(hand_contour):
		"""Fits an ellipse to the hand_contour

		:param hand_contour: np.array
		:return: ellipse as [(x,y),(semimajor-axis, semiminor-axis), angle]
		"""
		if len(hand_contour) > 5:
			return cv2.fitEllipse(hand_contour)
		return None

	def get_hand_vector(self, hand_contour):
		"""
		NOT IMPLEMENTED
		Will return a vector containing all the values describing the hand pose.
		:param hand_contour:
		:return:
		"""
		raise NotImplementedError

	# if hand_contour is not None:
	# 	hand_ellipse = self.get_hand_ellipse(hand_contour)
	# 	if hand_ellipse is not None:
	# 		(x,y),(majAxis, minAxis), angle = hand_ellipse
	# 		return np.array([x, y, majAxis, minAxis, angle])
	# else:
	# 	return np.zeros((5,))

	def get_derivative_hand_vector(self, hand_vector, prev_hand_vector, dt):
		"""
		NOT IMPLEMENTED
		Will return the derivative of the hand vector

		:param hand_vector:
		:param prev_hand_vector:
		:param dt:
		:return:
		"""
		raise NotImplementedError

	# return (hand_vector-prev_hand_vector)*dt

	@staticmethod
	def get_hand_roi(image, hand_contour):
		"""
		Returns the region of interest containing the hand_contour.

		:param image: np.array
		:param hand_contour: np.array
		:return: np.array
		"""
		x, y, w, h = cv2.boundingRect(hand_contour)
		return image[y:y + h, x:x + w]

	def detect_finger_tips(self, hand_contour):
		"""
		Detects the finger tips by computing the first and second derivatives of the distance of the contour point
		from the centroid with respect to the distance along the perimeter of the contour. These are then used
		to find points near local maxima, and then we filter out points that are too close to the centroid, and group clusters
		of points.

		:param hand_contour: np.array
		:return: list of np.array Represents the fingertips
		"""
		finger_tip_points = []
		center = self.get_hand_center(hand_contour)
		area = cv2.contourArea(hand_contour)
		radius = int((area / 3) ** 0.5 * 1.28)

		for i in range(len(hand_contour)):
			point0 = hand_contour[(i - 1) % len(hand_contour)]
			point1 = hand_contour[i]
			point2 = hand_contour[(i + 1) % len(hand_contour)]

			rpoint0 = cartesian_to_radial(point0, center)
			rpoint1 = cartesian_to_radial(point1, center)
			rpoint2 = cartesian_to_radial(point2, center)

			d01 = get_distance_between_points(point1, point0)
			d12 = get_distance_between_points(point2, point1)

			dr_dt0 = (rpoint1[0] - rpoint0[0]) / d01
			dr_dt1 = (rpoint2[0] - rpoint1[0]) / d12
			avg_dr_dt = (dr_dt0 + dr_dt1) / 2
			ddr_dt = (dr_dt1 - dr_dt0) / (d01 + d12)
			if abs(ddr_dt) < 0.2 and abs(avg_dr_dt) < 0.7 and rpoint1[0] > radius:
				if len(finger_tip_points) > 0 and np.linalg.norm(finger_tip_points[-1] - point1) < radius / 5:
					finger_tip_points[-1] = (point1 + finger_tip_points[-1]) / 2
				elif len(finger_tip_points) > 0 and np.linalg.norm(finger_tip_points[0] - point1) < radius / 5:
					finger_tip_points[0] = (point1 + finger_tip_points[0]) / 2
				else:
					finger_tip_points.append(point1)

		return finger_tip_points

	@staticmethod
	def detect_hand_contour(mask):
		"""
		Returns the largest contour in the mask (if the area is greater than 100 square pixels).
		:param mask: np.array
		:return: np.array
		"""

		# CHAIN_APPROX_TC89_L1 allows us to find the fingertips more accurately by approximating the curvature
		# of the fingertips.
		_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

		sorted_contours = sorted(contours, key=lambda cnt: cv2.contourArea(cnt), reverse=True)
		if len(sorted_contours) > 0:
			hand_contour = sorted_contours[0]
			if cv2.contourArea(hand_contour) < 100:
				return None
		else:
			return None
		return hand_contour


def main():
	out = cv2.VideoWriter('output.avi', -1, 30.0, (640, 360))

	purple_detector = ColorFinder("purple", hsv_color(143, 0, 0), hsv_color(215, 255, 225), True)
	hand_detector = HandDetector()

	cap = cv2.VideoCapture(1)

	# Enclose everything with try so that everything is properly cleaned up on errors.
	try:
		while True:
			t = time.time()

			# Read a frame from the VideoCapture and resize.
			ret, frame_bgr = cap.read()
			frame_bgr = cv2.resize(frame_bgr, (640, 360))
			if not ret:
				print("End of stream")
				break

			# Convert to HSV, then obtain mask from ColorFinder
			frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV_FULL)
			mask = purple_detector.find_color(frame_hsv, True)

			# Find hand contour in mask.
			hand_contour = hand_detector.detect_hand_contour(mask)

			# Draw hand measurements is a hand contour has been found.
			if hand_contour is not None:
				hand_pos = hand_detector.get_hand_center(hand_contour)
				cv2.circle(frame_bgr, (int(hand_pos[0]), int(hand_pos[1])), 5, (0, 0, 255), -1)

				cv2.drawContours(frame_bgr, [hand_contour], 0, (0, 0, 255), 2)

				# Find and draw fingertips.
				finger_tips = hand_detector.detect_finger_tips(hand_contour)
				for p in finger_tips:
					cv2.circle(frame_bgr, (int(p[0][0]), int(p[0][1])), 5, (0, 255, 0), -1)

			# Frame rate calculations
			dt = time.time() - t
			fps = 1 / dt

			# Display frame rate in upper left corner
			cv2.putText(frame_bgr, "FPS: " + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

			# Show frame and write to file.
			cv2.imshow("image", frame_bgr)
			out.write(frame_bgr)

			# Check if 'Escape' key has been pressed. This function causes a 30 ms delay!
			k = cv2.waitKey(30) & 0xff
			if k == 27:
				break

			print(fps)

	# Clean up
	finally:
		cap.release()
		out.release()
		cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
