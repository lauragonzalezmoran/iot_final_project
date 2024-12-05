import time
import threading

from pulse_oximeter_reader import initialize_pulse_oximeter, get_pulse_oximeter_data # ...
from night_vision_camera import initialize_camera, monitor_motion, face_detection # ...
from alarm import alarma, stop_alarma

# ===========================
# Global Variables and Config
# ===========================
DATA_LOG_INTERVAL = 1  # seconds between data logs
ALERT_THRESHOLD_OXYGEN = 30  # % SpO2 threshold for alert
ALERT_THRESHOLD_HEART_RATE = 50  # bpm threshold for alert (too low)

# ===========================
# Alert System
# ===========================
def trigger_alert(message):
    """
    Triggers an alert based on the input message.
    """
    print(f"ALERT: {message}")
    # TODO: Implement a more robust alert system (e.g., sound, notification, etc.)
    archivo_mp3 = "alarm.wav"  # Cambia esto por la ruta de tu archivo MP3
    alarma(archivo_mp3)
    time.sleep(10)  # Deja que la alarma suene por 10 segundos
    stop_alarma()

# ===========================
# Data Logger
# ===========================
def log_data(heart_rate, oxygen_level, face_detected):
    """
    Logs the collected data to a file.
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
    """
    print("Starting sleep monitoring...")
    # Initialize devices
    m = initialize_pulse_oximeter()
    initialize_camera()

    while True:
        # Get pulse oximeter data
        oxygen_level, oxygen_level_ok, heart_rate, heart_rate_ok = get_pulse_oximeter_data(m)

        # Check for abnormal values
        if oxygen_level == -999 or oxygen_level < ALERT_THRESHOLD_OXYGEN:
            trigger_alert(f"Low Oxygen Level: {oxygen_level}%")
        if heart_rate  == -999 or heart_rate < ALERT_THRESHOLD_HEART_RATE:
            trigger_alert(f"Low Heart Rate: {heart_rate} bpm")
        else:
            print( "Baby Vital Signs OK")
        # Monitor motion from camera
        face_detected = face_detection()
        if face_detected:
            print("Face detected, No Risk of Asphyxia")
        else:
            print("Warning!! Risk of Asphyxia")

        # Log data at intervals
        log_data(heart_rate, oxygen_level, face_detected)
        time.sleep(DATA_LOG_INTERVAL)


# ===========================
# Multi-threading Setup
# ===========================
def run_multithreaded():
    """
    Runs the monitoring system using multiple threads for performance.
    """
    monitor_thread = threading.Thread(target=monitoring_loop)
    monitor_thread.start()
    monitor_thread.join()


if __name__ == "__main__":
    try:
        run_multithreaded()
    except KeyboardInterrupt:
        print("Shutting down monitoring system...")
