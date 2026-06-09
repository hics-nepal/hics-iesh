#!/usr/bin/env python3
"""Standalone test for SH1106 OLED display on I2C 0x3C.
   Cycles through several test patterns so you can visually confirm the screen works."""
import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

PASSES = 0
FAILS = 0

print("=== OLED Test (SH1106, I2C 0x3C) ===")

try:
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial, width=128, height=64)
    print("Init:   PASS")
    PASSES += 1
except Exception as e:
    print(f"Init:   FAIL  [{e}]")
    FAILS += 1
    device = None

if device:
    tests = [
        ("Text screen",   lambda draw: (draw.text((0, 0), "=== IESH OLED ===", fill="white"),
                                        draw.text((0, 14), "OLED Test Active", fill="white"),
                                        draw.text((0, 28), "Line 3: 128x64 px", fill="white"),
                                        draw.text((0, 42), "All systems check", fill="white"))),
        ("Border box",    lambda draw: draw.rectangle((0, 0, 127, 63), outline="white")),
        ("Cross / diag",  lambda draw: (draw.line((0, 0, 127, 63), fill="white"),
                                        draw.line((127, 0, 0, 63), fill="white"))),
        ("Full fill",     lambda draw: draw.rectangle((0, 0, 127, 63), fill="white")),
        ("Clear",         lambda draw: None),
    ]

    for name, fn in tests:
        try:
            with canvas(device) as draw:
                fn(draw)
            print(f"  {name:<20} PASS")
            PASSES += 1
            time.sleep(1.5)
        except Exception as e:
            print(f"  {name:<20} FAIL  [{e}]")
            FAILS += 1

    device.clear()

print(f"\nResult: {PASSES} passed, {FAILS} failed")
import sys
sys.exit(0 if FAILS == 0 else 1)
