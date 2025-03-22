import cv2
import numpy as np
import time

# Initialize the video capture
cap = cv2.VideoCapture(0)
time.sleep(3)  # Allow camera to adjust

# Capture the background frame multiple times for stability
for i in range(30):
    ret, background = cap.read()
if not ret:
    print("Error capturing background")
    cap.release()
    cv2.destroyAllWindows()
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for natural view
    frame = cv2.flip(frame, 1)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color range for detecting red cloak (tune if needed)
    lower_red1 = np.array([0, 120, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 50])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color detection
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Refine mask using morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Create inverse mask
    mask_inv = cv2.bitwise_not(mask)

    # Extract background where cloak is present
    cloak_area = cv2.bitwise_and(background, background, mask=mask)

    # Extract foreground without the cloak
    foreground = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Smooth blending for better effect
    output = cv2.addWeighted(cloak_area, 1, foreground, 1, 0)

    # Display the output
    cv2.imshow("Invisibility Cloak", output)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
