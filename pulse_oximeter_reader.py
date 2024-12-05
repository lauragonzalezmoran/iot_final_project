import max30102
import hrcalc


def initialize_pulse_oximeter():
    m = max30102.MAX30102()
    return m
# 100 samples are read and used for HR/SpO2 calculation in a single loop
def get_pulse_oximeter_data(m):
    red, ir = m.read_sequential()
    print(hrcalc.calc_hr_and_spo2(ir, red))
    return hrcalc.calc_hr_and_spo2(ir, red)


'''m=initialize_pulse_oximeter()
oxygen_level, oxygen_level_ok, heart_rate, heart_rate_ok = get_pulse_oximeter_data(m)
print(oxygen_level)
print(oxygen_level_ok)
print(heart_rate)
print(heart_rate_ok)'''
