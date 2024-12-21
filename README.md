# Baby Monitoring System

This project is a baby monitoring system that uses a pulse oximeter and a night vision camera to detect vital signs and potential risks of suffocation. The system logs data in real-time and triggers an alarm if dangerous conditions are detected.

## Repository Structure

- `main.py`: Main file that starts the monitoring system and coordinates the different functions.
- `alarm.py`: Module that handles the activation and deactivation of the sound alarm.
- `haarcascade_frontalface_default (1).xml`: XML file containing the Haar classifier for face detection.
- `hrcalc.py`: Module that provides functions to calculate heart rate (HR) and blood oxygen saturation (SpO2) from sensor data.
- `max30102.py`: Module that provides an interface for the MAX30102 pulse oximeter sensor.
- `night_vision_camera.py`: Module that initializes the night vision camera and monitors motion and face detection.
- `pulse_oximeter_reader.py`: Module that initializes the pulse oximeter and obtains real-time data.
- `sleep_monitor_log.csv`: Output file where monitoring data is logged.
- `.gitignore`: File specifying which files should be ignored by Git.

## Running the Code

To run the monitoring system, follow these steps:

1. Ensure you have the necessary dependencies installed, such as `pygame` and `RPi.GPIO`.
2. Run the `main.py` file:
   ```sh
   python main.py

## Input File Formats
- haarcascade_frontalface_default (1).xml: XML file used for face detection.

## Output Files
- sleep_monitor_log.csv: CSV file where real-time monitoring data is logged, including heart rate, oxygen saturation, and face detection.
Hardcoded Addresses

In main.py, the path to the alarm sound file is hardcoded as alarm.wav. Replace this path with the location of your alarm sound file.

## Hardware

The system is designed to run on a Raspberry Pi environment with a MAX30102 sensor and a night vision camera. Connect the camera to the rashberry pi and also connect the pin to the pulse-oximeter pcb as indicated below.

Before running, enable i2c interface, install smbus and rpi.gpio, and connect the sensor.
> ⚠️ **Warning**: Ensure that sense hat is not connected for the I2C to work.

#### Port Connections:

| RPi                     | HR Sensor |
| ----------------------- | --------- |
| 3.3V (pin1)             | VIN       |
| I2C_SDA1 (pin3; GPIO 2) | SDA       |
| I2C_SCL1 (pin5; GPIO 3) | SCL       |
| - (pin7; GPIO 4)        | INT       |
| GND (pin9)              | GND       |

The code requires all 5 pins to work correctly. Please ensure that INT pin is connected.

If you have any questions or need more information, feel free to contact us.

