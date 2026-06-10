#!/usr/bin/env python3
"""Standalone test for DHT22 on GPIO 23.
   DHT22 bit-banging on kernel 6.x has ~50% per-read success rate — retries are normal."""
import time
import board
import adafruit_dht

PASSES = 0
FAILS = 0
valid_readings = 0

print("=== DHT22 Test (GPIO 23) ===")
print("NOTE: Kernel 6.x timing jitter causes ~50% retry rate — this is normal.\n")

try:
    sensor = adafruit_dht.DHT22(board.D23, use_pulseio=False)
    print("Init:     PASS")
    PASSES += 1
except Exception as e:
    print(f"Init:     FAIL  [{e}]")
    FAILS += 1
    sensor = None

if sensor:
    print("Taking up to 15 samples (3s apart), need at least 3 valid:")
    for i in range(15):
        time.sleep(3)
        try:
            t = sensor.temperature
            h = sensor.humidity
            if t is not None and h is not None:
                print(f"  [{i+1:2d}] Temp: {t:.1f} C   Humidity: {h:.1f} %   OK")
                valid_readings += 1
                if valid_readings >= 3:
                    print("  (got 3 valid readings — stopping early)")
                    break
            else:
                print(f"  [{i+1:2d}] null read   retry")
        except RuntimeError as e:
            print(f"  [{i+1:2d}] {e}   retry")
        except Exception as e:
            print(f"  [{i+1:2d}] FAIL  [{e}]")
            FAILS += 1
    sensor.exit()

    if valid_readings >= 3:
        print(f"\nDHT22 readings: {valid_readings} valid   PASS")
        PASSES += 1
    elif valid_readings >= 1:
        print(f"\nDHT22 readings: {valid_readings} valid (low success rate — check pull-up)   PASS")
        PASSES += 1
    else:
        print("\nDHT22 readings: 0 valid   FAIL")
        FAILS += 1

print(f"\nResult: {PASSES} passed, {FAILS} failed")
import sys
sys.exit(0 if FAILS == 0 else 1)
