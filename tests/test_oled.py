#!/usr/bin/env python3
"""Standalone test for SH1106 OLED display on I2C 0x3C.
   Uses direct smbus2 writes (bypasses luma i2c_rdwr which fails on this module)."""
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from sensors.oled import OLED

PASSES = 0
FAILS = 0

print("=== OLED Test (SH1106, I2C 0x3C) ===")

oled = OLED()
if oled.ok:
    print("Init:   PASS")
    PASSES += 1
else:
    print(f"Init:   FAIL  [{oled.error}]")
    FAILS += 1

if oled.ok:
    tests = [
        ("Text screen",  lambda draw: [
            draw.text((0,  0), "=== IESH OLED ===", fill="white"),
            draw.text((0, 14), "OLED Test Active",  fill="white"),
            draw.text((0, 28), "128x64 direct i2c", fill="white"),
            draw.text((0, 42), "All systems check", fill="white"),
        ]),
        ("Border box",   lambda draw: draw.rectangle((0, 0, 127, 63), outline="white")),
        ("Cross / diag", lambda draw: [
            draw.line((0, 0, 127, 63), fill="white"),
            draw.line((127, 0, 0, 63), fill="white"),
        ]),
        ("Full fill",    lambda draw: draw.rectangle((0, 0, 127, 63), fill="white")),
        ("Clear",        lambda draw: None),
    ]

    for name, fn in tests:
        try:
            with oled.canvas() as draw:
                fn(draw)
            print(f"  {name:<20} PASS")
            PASSES += 1
            time.sleep(1.5)
        except Exception as e:
            print(f"  {name:<20} FAIL  [{e}]")
            FAILS += 1

    oled.clear()

print(f"\nResult: {PASSES} passed, {FAILS} failed")
sys.exit(0 if FAILS == 0 else 1)
