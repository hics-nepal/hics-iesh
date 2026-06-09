#!/usr/bin/env python3
"""Standalone test for MQ-7 (CO) and MQ-135 (AQI) gas sensors via MCP3208.
   Runs for 30 seconds — sensors need warm-up time before readings stabilise."""
import spidev
import time

CH_MQ7   = 0   # change if wired differently
CH_MQ135 = 1   # change if wired differently
VREF     = 3.3

PASSES = 0
FAILS = 0

print("=== MQ Gas Sensor Test (MCP3208) ===")
print(f"MQ-7  on CH{CH_MQ7}, MQ-135 on CH{CH_MQ135}")
print("NOTE: Gas sensors need 20-30s warm-up. Readings will stabilise over time.\n")

try:
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1_000_000
    print("SPI init:   PASS")
    PASSES += 1
except Exception as e:
    print(f"SPI init:   FAIL  [{e}]")
    spi = None
    FAILS += 1

def read_ch(ch):
    cmd = [0x06 | (ch >> 2), (ch & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

if spi:
    print("Sampling every 2s for 30s (watch for stable non-zero values):\n")
    print(f"{'Time':>6}  {'MQ-7 raw':>10}  {'MQ-7 V':>8}  {'MQ-135 raw':>12}  {'MQ-135 V':>10}")
    print("-" * 60)
    for i in range(15):
        t = i * 2
        try:
            raw7   = read_ch(CH_MQ7)
            raw135 = read_ch(CH_MQ135)
            v7     = (raw7   * VREF) / 4095
            v135   = (raw135 * VREF) / 4095
            status = "PASS" if raw7 > 0 and raw135 > 0 else "WARN (0 reading)"
            print(f"{t:>5}s  {raw7:>10d}  {v7:>7.3f}V  {raw135:>12d}  {v135:>9.3f}V  {status}")
            if raw7 > 0 and raw135 > 0:
                PASSES += 1
        except Exception as e:
            print(f"{t:>5}s  FAIL [{e}]")
            FAILS += 1
        time.sleep(2)

    print("\nAll-channel scan (if all zeros, MCP3208 wiring issue — MISO/CS/VREF):")
    for ch in range(8):
        cmd = [0x06 | (ch >> 2), (ch & 0x03) << 6, 0x00]
        r = spi.xfer2(cmd)
        v = ((r[1] & 0x0F) << 8) | r[2]
        flag = " <-- non-zero" if v > 10 else ""
        print(f"  CH{ch}: {v:4d}{flag}")
    spi.close()

print(f"\nResult: {PASSES} passed, {FAILS} failed")
print("Expected: raw values in range 100-4000, voltage 0.1-3.3V after warm-up.")
import sys
sys.exit(0 if PASSES > 1 else 1)
