#!/usr/bin/env python3
"""Sync system time to DS3231 RTC. Run after setting Pi time via NTP."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensors.rtc import RTC
from datetime import datetime

rtc = RTC()
if not rtc.ok:
    print(f"RTC init failed: {rtc.error}")
    sys.exit(1)

now = datetime.now()
if rtc.sync_from_system():
    print(f"RTC synced to: {now.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    print(f"Sync failed: {rtc.error}")
    sys.exit(1)
