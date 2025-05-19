import cv2
import numpy as np
import math

# Read the image
image = cv2.imread('Experiment_Images/clearsky.jpg')

# Get the dimensions of the image
height, width, _ = image.shape

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply binary thresholding
_, thresholded_image = cv2.threshold(gray_image, 220, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Function to compute the centroid of a contour
def get_centroid(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    return (cX, cY)

# Specify the reference point (center extreme bottom of the image)
reference_point = (width // 2, height - 1)

# Calculate the distance and angle from each centroid to the reference point
measurements = []
for contour in contours:
    centroid = get_centroid(contour)
    # Distance (in pixels)
    distance = np.sqrt((centroid[0] - reference_point[0])**2 + (centroid[1] - reference_point[1])**2)
    # Angle in radians
    angle = math.atan2(reference_point[1] - centroid[1], centroid[0] - reference_point[0])
    # Convert angle to degrees
    angle_degrees = math.degrees(angle)
    measurements.append((centroid, distance, angle_degrees))

# Print the distances and angles
for i, (centroid, distance, angle_degrees) in enumerate(measurements):
    print(f"Contour {i}: Centroid = {centroid}, Distance = {distance:.2f} pixels, Angle = {angle_degrees:.2f} degrees")

# Optionally, draw the reference point, centroids, lines, and labels on the image
output_image = image.copy()
cv2.circle(output_image, reference_point, 5, (0, 0, 255), -1)  # Red dot for reference point
for i, (centroid, distance, angle_degrees) in enumerate(measurements):
    cv2.circle(output_image, centroid, 5, (255, 0, 0), -1)  # Blue dots for centroids
    cv2.line(output_image, reference_point, centroid, (0, 255, 0), 2)  # Green lines
    # Label the contour
    cv2.putText(output_image, f"{i}", (centroid[0] + 10, centroid[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

# Display the image with centroids, reference point, lines, and labels
cv2.imshow('Centroids, Reference Point, Lines, and Labels', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Optional: Save the result
#cv2.imwrite('output_image.png', output_image)
