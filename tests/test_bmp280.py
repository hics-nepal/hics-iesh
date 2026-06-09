#!/usr/bin/env python3
"""Standalone test for BMP280. Tries both I2C addresses (0x76 and 0x77)."""
import sys
import smbus2
from bmp280 import BMP280

PASSES = 0
FAILS = 0

print("=== BMP280 Test (I2C, trying 0x76 and 0x77) ===")

bus = smbus2.SMBus(1)
bmp = None
found_addr = None

for addr in [0x76, 0x77]:
    try:
        bmp = BMP280(i2c_dev=bus, i2c_addr=addr)
        # Quick sanity — a valid read means the chip responded
        t = bmp.get_temperature()
        if t is not None:
            print(f"Init at 0x{addr:02X}: PASS")
            found_addr = addr
            PASSES += 1
            break
    except Exception as e:
        print(f"Init at 0x{addr:02X}: FAIL  [{e}]")
        bmp = None

if found_addr is None:
    FAILS += 1
    print("BMP280 not found at 0x76 or 0x77.")
    print("Check: SDA->GPIO2 (pin 3), SCL->GPIO3 (pin 5), VCC->3.3V, SDO pin pulled to GND for 0x76 or 3.3V for 0x77")

if bmp:
    try:
        temp = bmp.get_temperature()
        print(f"Temperature: {temp:.2f} C   PASS")
        PASSES += 1
    except Exception as e:
        print(f"Temperature: FAIL  [{e}]")
        FAILS += 1

    try:
        pres = bmp.get_pressure()
        print(f"Pressure:    {pres:.2f} hPa   PASS")
        PASSES += 1
        if found_addr != 0x76:
            print(f"  NOTE: update BMP280_ADDR in sensors/config.py to 0x{found_addr:02X}")
    except Exception as e:
        print(f"Pressure:    FAIL  [{e}]")
        FAILS += 1

print(f"\nResult: {PASSES} passed, {FAILS} failed")
sys.exit(0 if FAILS == 0 else 1)
