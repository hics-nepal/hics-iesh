#!/usr/bin/env python3
"""Interactive soil moisture calibration. Run this on the RPI and update
SOIL_DRY / SOIL_WET in sensors/config.py with the printed values."""
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1_000_000

CHANNEL = 2  # CH2 — must match CH_SOIL in config.py

def read():
    cmd = [0x06 | (CHANNEL >> 2), (CHANNEL & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

print("=== HICS Soil Calibration ===")
print(f"Reading from MCP3208 CH{CHANNEL}\n")

input("Step 1: Hold sensor in DRY AIR, then press Enter...")
readings = [read() for _ in range(10)]
dry_val = int(sum(readings) / len(readings))
print(f"--> DRY baseline (averaged): {dry_val}\n")

input("Step 2: Submerge sensor tip in water, then press Enter...")
readings = [read() for _ in range(10)]
wet_val = int(sum(readings) / len(readings))
print(f"--> WET baseline (averaged): {wet_val}\n")

print("Update sensors/config.py:")
print(f"  SOIL_DRY = {dry_val}")
print(f"  SOIL_WET = {wet_val}")
spi.close()
