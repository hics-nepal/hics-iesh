#!/usr/bin/env python3
"""Test RPi Camera v1.3 (OV5647) — capture and sky analysis."""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sensors.camera import capture_sky, sky_analysis, DEFAULT_PATH

PASS = True

print("=" * 50)
print(" Camera (OV5647) Test")
print("=" * 50)

# Test 1: capture
print("\n[1] Capture sky frame...")
ok = capture_sky(DEFAULT_PATH, width=640, height=480)
if ok:
    size_kb = os.path.getsize(DEFAULT_PATH) // 1024
    print(f"    PASS  Saved to {DEFAULT_PATH}  ({size_kb} KB)")
else:
    print("    FAIL  rpicam-still returned error or file too small")
    PASS = False

# Test 2: sky analysis
print("\n[2] Sky analysis...")
if ok:
    info = sky_analysis(DEFAULT_PATH)
    required = ['brightness', 'cloud_cover_pct', 'condition', 'captured_at']
    missing = [k for k in required if k not in info]
    if missing:
        print(f"    FAIL  Missing keys: {missing}")
        PASS = False
    elif info['brightness'] is None:
        print("    WARN  Pillow not installed — analysis skipped (install python3-pil)")
    else:
        print(f"    PASS  brightness={info['brightness']}  cloud={info['cloud_cover_pct']}%  condition={info['condition']}")
else:
    print("    SKIP  (no image to analyse)")

print()
print("=" * 50)
print(f" Result: {'PASS' if PASS else 'FAIL'}")
print("=" * 50)
sys.exit(0 if PASS else 1)
