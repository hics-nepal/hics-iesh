#!/usr/bin/env python3
"""Standalone test for capacitive soil moisture sensor via MCP3208.
   Reports raw ADC values so you can verify calibration values in config.py."""
import spidev
import time

SOIL_DRY = 4018   # from config — update if you recalibrate
SOIL_WET = 2084
CHANNEL  = 2      # CH2 — change to match your physical wiring

PASSES = 0
FAILS = 0

print("=== Soil Moisture Test (MCP3208) ===")
print(f"Reading from channel CH{CHANNEL}")
print(f"Calibration: DRY={SOIL_DRY}, WET={SOIL_WET}")
print()

try:
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1_000_000
    print("SPI init:   PASS")
    PASSES += 1
except Exception as e:
    print(f"SPI init:   FAIL  [{e}]")
    FAILS += 1
    spi = None

def read_ch(ch):
    cmd = [0x06 | (ch >> 2), (ch & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

if spi:
    print("Taking 5 readings:")
    for i in range(5):
        try:
            raw = read_ch(CHANNEL)
            pct = max(0, min(100, ((SOIL_DRY - raw) / (SOIL_DRY - SOIL_WET)) * 100))
            print(f"  [{i+1}] Raw: {raw:4d}  ->  {pct:5.1f}%   PASS")
            PASSES += 1
        except Exception as e:
            print(f"  [{i+1}] FAIL  [{e}]")
            FAILS += 1
        time.sleep(0.5)

    # Scan all channels before closing — helps locate sensor if on wrong channel
    print("\nAll-channel scan:")
    for ch in range(8):
        cmd = [0x06 | (ch >> 2), (ch & 0x03) << 6, 0x00]
        r = spi.xfer2(cmd)
        v = ((r[1] & 0x0F) << 8) | r[2]
        flag = " <-- non-zero, sensor likely here" if v > 10 else ""
        print(f"  CH{ch}: {v:4d}{flag}")
    spi.close()

print(f"\nResult: {PASSES} passed, {FAILS} failed")
if FAILS > 0 or (spi and all(True for _ in range(1))):
    if PASSES > 1:
        print("NOTE: Raw=0 on all channels means MCP3208 wiring issue (MISO stuck low or CS not connected)")

import sys
sys.exit(0 if FAILS == 0 else 1)
