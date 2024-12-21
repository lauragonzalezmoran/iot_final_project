import cv2
from picamera2 import Picamera2
import numpy as np

# ===========================
# Night Vision Camera Module
# ===========================
"""
This module manages the night vision camera and its functionalities within the baby monitoring system.
Its primary role is to detect motion and faces in real time, enabling the system to identify potential risks 
of asphyxia based on movement patterns and the presence of the baby. The module integrates with the 
pulse oximeter and alarm components to provide a comprehensive monitoring solution.
"""

# ===========================
# Global Variables
# ===========================
camera = None  # Camera object for capturing frames
back_sub = None  # Background subtractor for motion detection
kernel_open = np.ones((5, 5), np.uint8)  # Kernel for morphological opening
kernel_dilate = np.ones((10, 10), np.uint8)  # Kernel for dilation

# ===========================
# Night Vision Camera Functions
# ===========================
def initialize_camera():
    """
    Initializes the night vision camera and configures it for real-time monitoring.
    
    This function sets up the camera resolution, format, and background subtractor 
    for motion detection.
    """
    global camera, back_sub
    print("Initializing night vision camera...")

    # Initialize the Picamera2 object
    camera = Picamera2()
    camera.preview_configuration.main.size = (640, 360)  # Set resolution
    camera.preview_configuration.main.format = "RGB888"  # Set color format
    camera.preview_configuration.align()
    camera.configure("preview")  # Configure the camera for preview mode
    camera.start()

    # Create a background subtractor for motion detection
    back_sub = cv2.createBackgroundSubtractorMOG2(
        history=100, varThreshold=15, detectShadows=False
    )

def monitor_motion():
    """
    Detects motion using the night vision camera feed.

    This function applies background subtraction and contour analysis to determine 
    if motion is present in the frame. The size of detected contours is used to 
    filter noise.

    Returns:
    bool: True if motion is detected, False otherwise.
    """
    global camera, back_sub, kernel_open, kernel_dilate

    motion_detected = False

    # Capture a frame from the camera
    frame = camera.capture_array()

    # Convert the frame to grayscale and enhance contrast
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    equilized = cv2.equalizeHist(gray)

    # Apply background subtraction
    fgmask = back_sub.apply(equilized)

    # Perform morphological operations to clean up the mask
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel_open)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_DILATE, kernel_dilate)

    # Threshold the mask to extract binary regions
    _, thresh = cv2.threshold(fgmask, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze contours to detect significant motion
    for contour in contours:
        if cv2.contourArea(contour) > 5000:  # Adjust threshold as needed
            motion_detected = True

    return motion_detected

def face_detection():
    """
    Detects faces in the camera feed using Haar cascades.

    This function analyzes the camera frames for the presence of faces, which helps 
    confirm the baby's presence in the monitored area and assess asphyxia risk.

    Returns:
    bool: True if a face is detected, False otherwise.
    """
    global camera
    face_cascade = cv2.CascadeClassifier(
        '/home/pi/Documents/finalproject/iot_final_project/haarcascade_frontalface_default (1).xml'
    )

    face_detected = False

    # Capture a frame from the camera
    frame = camera.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # Convert to grayscale

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=4
    )

    if len(faces) > 0:
        face_detected = True

    return face_detected

# Uncomment this block for testing the camera functions
'''
initialize_camera()
while True:
    face_detected = face_detection()
    if face_detected:
        print('Face detected.')
    else:
        print('No face detected.')
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        camera.stop()
        cv2.destroyAllWindows()
        break
'''
