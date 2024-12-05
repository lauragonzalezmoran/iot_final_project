import cv2
from picamera2 import Picamera2
import numpy as np

camera = None
back_sub = None
kernel_open = np.ones((5, 5), np.uint8)
kernel_dilate = np.ones((10, 10), np.uint8)

# ===========================
# Night Vision Camera Functions
# ===========================
def initialize_camera():
    """
    Initialize the night vision camera.
    """
    global camera, back_sub
    print("Initializing night vision camera...")
    # TODO: Add initialization code for the camera here

    camera = Picamera2()
    camera.preview_configuration.main.size = (640, 360)
    camera.preview_configuration.main.format = "RGB888"
    camera.preview_configuration.align()
    camera.configure("preview")
    camera.start()

    back_sub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=15, detectShadows=False)



def monitor_motion():
    """
    Captures a frame from the night vision camera and checks for motion.
    Returns: True if motion detected, False otherwise.
    """
    global camera, back_sub, kernel_open, kernel_dilate
    # TODO: Implement function to analyze motion from the camera feed

    motion_detected = False

    frame = camera.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    equilized = cv2.equalizeHist(gray)
    fgmask = back_sub.apply(equilized)

    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel_open)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_DILATE, kernel_dilate)

    _, thresh = cv2.threshold(fgmask, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 5000:  # Adjust the area threshold if needed
            motion_detected = True

    return motion_detected

def face_detection():
    """
    Captures a frame from the night vision camera and checks for faces.
    Returns: True if face detected, False otherwise.
    """
    global camera
    face_cascade = cv2.CascadeClassifier('/home/pi/Documents/finalproject/iot_final_project/haarcascade_frontalface_default (1).xml')

    # TODO: Implement function to analyze faces from the camera feed

    face_detected = False

    frame = camera.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    if len(faces)>0:
        face_detected = True

    return face_detected

'''initialize_camera()
while True:
    face_detected= face_detection()
    if face_detected:
        print('yes')
    else:
        print('no')
    if cv2.waitKey(1) & 0xFF==ord('q'):
        camera.stop()
        cv2.destroyAllWindows()
        break'''
    
'''
