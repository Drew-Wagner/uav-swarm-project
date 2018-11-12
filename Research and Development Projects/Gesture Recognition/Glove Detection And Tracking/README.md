# Glove Detection and Track

This program tracks a purple disposable glove, and will eventually be able to recognise hand gestures.

## How it works

The program first identifies a mask of pixels that are in the defined HSV color range for the purple glove. Then it uses OpenCV's built-in contour detection to find the largest contour, which the program expects to be the hand. Next the program calculates the Moments of the contour in order to find the centroid. The next step is to find the fingertips. This is done by calculating the first and second derivatives of the distance from from the point on the contour to the centroid with respect to the distance along the perimeter of the contour. Next points that are closer than a threshold (set according to the area of the contour) are filtered out, and finally points that are close together are grouped together as a single point.
