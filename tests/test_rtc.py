#!/usr/bin/env python3
"""Standalone test for DS3231 RTC on I2C 0x68."""
import smbus2
from datetime import datetime

RTC_ADDR = 0x68
I2C_BUS  = 1

PASSES = 0
FAILS = 0

def bcd_to_dec(b):
    return (b >> 4) * 10 + (b & 0x0F)

print("=== DS3231 RTC Test (I2C 0x68) ===")

try:
    bus = smbus2.SMBus(I2C_BUS)
    # Probe the device
    bus.read_byte_data(RTC_ADDR, 0x00)
    print("I2C probe:   PASS")
    PASSES += 1
except Exception as e:
    print(f"I2C probe:   FAIL  [{e}]")
    print("  Check: SDA on GPIO 2, SCL on GPIO 3, 3.3V power to RTC module")
    FAILS += 1
    bus = None

if bus:
    try:
        data   = bus.read_i2c_block_data(RTC_ADDR, 0x00, 7)
        sec    = bcd_to_dec(data[0] & 0x7F)
        minute = bcd_to_dec(data[1])
        hour   = bcd_to_dec(data[2] & 0x3F)
        day    = bcd_to_dec(data[4])
        month  = bcd_to_dec(data[5] & 0x1F)
        year   = bcd_to_dec(data[6]) + 2000
        rtc_dt = datetime(year, month, day, hour, minute, sec)
        sys_dt = datetime.now()
        delta  = abs((sys_dt - rtc_dt).total_seconds())
        print(f"RTC time:    {rtc_dt.strftime('%Y-%m-%d %H:%M:%S')}   PASS")
        print(f"System time: {sys_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Drift:       {delta:.0f} seconds {'(OK)' if delta < 120 else '(large — run sync_rtc.py)'}")
        PASSES += 1
    except Exception as e:
        print(f"Read time:   FAIL  [{e}]")
        FAILS += 1

print(f"\nResult: {PASSES} passed, {FAILS} failed")
import sys
sys.exit(0 if FAILS == 0 else 1)
