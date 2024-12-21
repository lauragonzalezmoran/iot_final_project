# ===========================
# Pulse Oximeter Reader Module
# ===========================
"""
This module is responsible for interfacing with the pulse oximeter sensor and extracting 
real-time data about the baby's oxygen saturation (SpO2) and heart rate (HR). It plays a 
critical role in the baby monitoring system by providing vital signs that are used to 
assess the baby's health and detect potential asphyxia risks. 

The module initializes the pulse oximeter hardware and processes the sensor data using 
signal processing algorithms to calculate SpO2 and HR values.

Libraries Used:
- max30102: Provides a Python interface for the MAX30102 pulse oximeter sensor, allowing 
  data retrieval from its red and infrared (IR) light sensors.
- hrcalc: Processes raw sensor data to calculate heart rate (HR) and blood oxygen saturation 
  (SpO2) using signal processing algorithms.
"""

# ===========================
# Import Libraries
# ===========================
import max30102  # Interface for the MAX30102 sensor to read red and IR light data
import hrcalc  # Provides functions to calculate HR and SpO2 from sensor data

# ===========================
# Functions
# ===========================

def initialize_pulse_oximeter():
    """
    Initializes the MAX30102 pulse oximeter sensor.

    This function creates an instance of the MAX30102 sensor, enabling communication 
    and data retrieval.

    Returns:
    max30102.MAX30102: An instance of the MAX30102 pulse oximeter sensor.
    """
    m = max30102.MAX30102()
    return m

def get_pulse_oximeter_data(m):
    """
    Reads data from the pulse oximeter and calculates heart rate (HR) and SpO2.

    This function retrieves sequential data from the pulse oximeter's red and IR sensors, 
    processes the data using `hrcalc`, and calculates the heart rate and oxygen saturation.

    Parameters:
    m (max30102.MAX30102): An initialized instance of the MAX30102 pulse oximeter sensor.

    Returns:
    tuple: A tuple containing the following:
        - oxygen_level (float): The calculated blood oxygen saturation (SpO2) percentage.
        - oxygen_level_ok (bool): Whether the SpO2 calculation is reliable.
        - heart_rate (float): The calculated heart rate in beats per minute (BPM).
        - heart_rate_ok (bool): Whether the heart rate calculation is reliable.
    """
    # Read red and IR sensor data sequentially
    red, ir = m.read_sequential()

    # Process the data to calculate HR and SpO2
    oxygen_level, oxygen_level_ok, heart_rate, heart_rate_ok = hrcalc.calc_hr_and_spo2(ir, red)

    # Print calculated values for debugging purposes
    print(f"SpO2: {oxygen_level}% (Valid: {oxygen_level_ok}), HR: {heart_rate} BPM (Valid: {heart_rate_ok})")

    return oxygen_level, oxygen_level_ok, heart_rate, heart_rate_ok

# ===========================
# Testing (Commented Out)
# ===========================
'''
# Example usage for testing the pulse oximeter module
if __name__ == "__main__":
    # Initialize the pulse oximeter
    m = initialize_pulse_oximeter()

    # Retrieve and print heart rate and SpO2 data
    oxygen_level, oxygen_level_ok, heart_rate, heart_rate_ok = get_pulse_oximeter_data(m)
    print(f"SpO2: {oxygen_level}% (Valid: {oxygen_level_ok})")
    print(f"Heart Rate: {heart_rate} BPM (Valid: {heart_rate_ok})")
'''
