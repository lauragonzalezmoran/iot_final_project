import time
import threading

from pulse_oximeter_reader import initialize_pulse_oximeter, get_pulse_oximeter_data  # Replace with actual imports
from night_vision_camera import initialize_camera, monitor_motion, face_detection  # Replace with actual imports
from alarm import alarma, stop_alarma

# ===========================
# Global Variables and Config
# ===========================
DATA_LOG_INTERVAL = 1  # Seconds between data logs
ALERT_THRESHOLD_OXYGEN = 30  # % SpO2 threshold for alert
ALERT_THRESHOLD_HEART_RATE = 50  # bpm threshold for alert (too low)

# ===========================
# Alert System
# ===========================
def trigger_alert(message):
    """
    Triggers an alert based on the input message.

    This function activates the alarm system and logs the alert message.
    """
    print(f"ALERT: {message}")
    archivo_mp3 = "alarm.wav"  # Replace this with the path to your alarm sound file
    alarma(archivo_mp3)  # Sound the alarm
    time.sleep(10)  # Allow the alarm to sound for 10 seconds
    stop_alarma()  # Stop the alarm

# ===========================
# Data Logger
# ===========================
def log_data(heart_rate, oxygen_level, face_detected):
    """
    Logs real-time data of the baby's vital signs into a file, enabling the asphyxia detection algorithm to be refined
    based on personalized normal vital sign ranges. 

    Parameters:
    - heart_rate (int): Measured heart rate in bpm.
    - oxygen_level (int): Measured blood oxygen saturation (SpO2) in percentage.
    - face_detected (bool): Indicates if a face was detected.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("sleep_monitor_log.csv", "a") as log_file:
        log_file.write(f"{timestamp},{heart_rate},{oxygen_level},{face_detected}\n")
    print(f"Logged data: HR={heart_rate}, SpO2={oxygen_level}, Face={face_detected}")

# ===========================
# Main Monitoring Loop
# ===========================
def monitoring_loop():
    """
    Main loop that continuously monitors heart rate, SpO2, and motion.

    This function integrates data from the pulse oximeter and the camera to detect potential
    risks and triggers alerts when thresholds are crossed.
    """
    print("Starting sleep monitoring...")
    # Initialize devices
    m = initialize_pulse_oximeter()  # Initialize the pulse oximeter
    initialize_camera()  # Initialize the camera

    while True:
        # Get pulse oximeter data
        oxygen_level, oxygen_level_ok, heart_rate, heart_rate_ok = get_pulse_oximeter_data(m)

        # Check for abnormal values
        if oxygen_level == -999 or oxygen_level < ALERT_THRESHOLD_OXYGEN:
            trigger_alert(f"Low Oxygen Level: {oxygen_level}%")
        if heart_rate == -999 or heart_rate < ALERT_THRESHOLD_HEART_RATE:
            trigger_alert(f"Low Heart Rate: {heart_rate} bpm")
        else:
            print("Baby's vital signs are within normal limits.")

        # Monitor motion from camera
        face_detected = face_detection()
        if face_detected:
            print("Face detected. No risk of asphyxia.")
        else:
            print("Warning! Risk of asphyxia detected.")

        # Log data at intervals
        log_data(heart_rate, oxygen_level, face_detected)
        time.sleep(DATA_LOG_INTERVAL)  # Wait before the next monitoring cycle

# ===========================
# Multi-threading Setup
# ===========================
def run_multithreaded():
    """
    Runs the monitoring system using multiple threads for performance.

    This ensures efficient operation of the monitoring loop and allows for
    simultaneous processing of different tasks.
    """
    monitor_thread = threading.Thread(target=monitoring_loop)
    monitor_thread.start()
    monitor_thread.join()

# ===========================
# Main Execution
# ===========================
if __name__ == "__main__":
    try:
        run_multithreaded()  # Start the monitoring system
    except KeyboardInterrupt:
        print("Shutting down the monitoring system...")
