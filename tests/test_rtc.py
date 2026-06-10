#!/usr/bin/env python3
"""Standalone test for DS3231 RTC on I2C 0x68."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from sensors.rtc import RTC
from datetime import datetime

PASSES = 0
FAILS = 0

print("=== DS3231 RTC Test (I2C 0x68) ===")

rtc = RTC()
if rtc.ok:
    print("I2C probe:   PASS")
    PASSES += 1
else:
    print(f"I2C probe:   FAIL  [{rtc.error}]")
    print("  Check: SDA on GPIO 2, SCL on GPIO 3, 3.3V power to RTC module")
    FAILS += 1

if rtc.ok:
    rtc_dt = rtc.read()
    if rtc_dt:
        sys_dt = datetime.now()
        delta  = abs((sys_dt - rtc_dt).total_seconds())
        print(f"RTC time:    {rtc_dt.strftime('%Y-%m-%d %H:%M:%S')}   PASS")
        print(f"System time: {sys_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Drift:       {delta:.0f} seconds {'(OK)' if delta < 120 else '(large — run sync_rtc.py)'}")
        PASSES += 1
    else:
        print(f"Read time:   FAIL  [{rtc.error}]")
        FAILS += 1

print(f"\nResult: {PASSES} passed, {FAILS} failed")
sys.exit(0 if FAILS == 0 else 1)
