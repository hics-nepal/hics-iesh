#!/usr/bin/env python3
"""Standalone test for DHT22 on GPIO 23. Takes 5 readings."""
import time
import board
import adafruit_dht

PASSES = 0
FAILS = 0

print("=== DHT22 Test (GPIO 23) ===")
try:
    sensor = adafruit_dht.DHT22(board.D23, use_pulseio=False)
    print("Init:     PASS")
    PASSES += 1
except Exception as e:
    print(f"Init:     FAIL  [{e}]")
    FAILS += 1
    sensor = None

if sensor:
    print("Reading 5 samples (2s apart, DHT22 min interval):")
    for i in range(5):
        time.sleep(2.5)
        try:
            t = sensor.temperature
            h = sensor.humidity
            if t is not None and h is not None:
                print(f"  [{i+1}] Temp: {t:.1f} C   Humidity: {h:.1f} %   PASS")
                PASSES += 1
            else:
                print(f"  [{i+1}] Null read (retry is normal)   WARN")
        except RuntimeError as e:
            print(f"  [{i+1}] RuntimeError: {e}   WARN")
        except Exception as e:
            print(f"  [{i+1}] FAIL  [{e}]")
            FAILS += 1
    sensor.exit()

print(f"\nResult: {PASSES} passed, {FAILS} failed")
if PASSES == 1 and FAILS == 0:
    print("WARNING: Init succeeded but no valid readings — check wiring (GPIO 23, 3.3V power, 10kΩ pull-up)")
import sys
sys.exit(0 if PASSES > 1 else 1)
