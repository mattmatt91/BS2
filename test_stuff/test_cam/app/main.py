import cv2
import os
from time import sleep
# Ensure the images directory exists
os.makedirs('app/images/', exist_ok=True)

# Initialize the camera
cap = cv2.VideoCapture(1)  # 0 is the default camera
# Capture a single frame
ret, frame = cap.read()
# Save the captured frame
if ret:
    print(frame)
    cv2.imwrite('images/captured_image2.jpg', frame)

# Release the capture
cap.release()
