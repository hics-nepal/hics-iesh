#!/usr/bin/env python3
"""Standalone test for DS18B20 soil temperature sensor on GPIO 4 (1-Wire)."""
import os
import glob
import time

PASSES = 0
FAILS = 0

print("=== DS18B20 Test (1-Wire, GPIO 4) ===")

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
time.sleep(0.5)

base_dir = '/sys/bus/w1/devices/'
folders = glob.glob(base_dir + '28*')

if folders:
    print(f"Found {len(folders)} sensor(s):   PASS")
    PASSES += 1
    for folder in folders:
        sensor_id = os.path.basename(folder)
        device_file = folder + '/w1_slave'
        print(f"  Sensor ID: {sensor_id}")
        try:
            with open(device_file, 'r') as f:
                lines = f.readlines()
            if lines[0].strip()[-3:] != 'YES':
                print(f"  CRC check: FAIL (bad wiring or pull-up resistor?)")
                FAILS += 1
            else:
                pos = lines[1].find('t=')
                temp = float(lines[1][pos + 2:]) / 1000.0
                print(f"  Temp:      {temp:.2f} C   PASS")
                PASSES += 1
        except Exception as e:
            print(f"  Read:      FAIL  [{e}]")
            FAILS += 1
else:
    print("No DS18B20 found.   FAIL")
    print("  Check: GPIO 4 wiring, 4.7kΩ pull-up to 3.3V, /boot/firmware/config.txt has dtoverlay=w1-gpio")
    FAILS += 1

print(f"\nResult: {PASSES} passed, {FAILS} failed")
import sys
sys.exit(0 if FAILS == 0 else 1)
