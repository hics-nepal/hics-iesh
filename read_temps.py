import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

def get_sensor_folders():
    return glob.glob(base_dir + '28*')

def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        return float(temp_string) / 1000.0

try:
    print("Initializing 1-Wire bus... Looking for sensors...")
    while True:
        device_folders = get_sensor_folders()
        if not device_folders:
            print("No sensors detected. Check your 4.7k resistor and wiring!")
            time.sleep(2)
            continue
        print("\n--- Temperature Reading ---")
        for i, folder in enumerate(device_folders):
            device_file = folder + '/w1_slave'
            sensor_id = os.path.basename(folder)
            temp = read_temp(device_file)
            print(f"Sensor {i+1} (ID: {sensor_id}): {temp:.2f} C")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
