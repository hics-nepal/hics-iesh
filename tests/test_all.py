#!/usr/bin/env python3
"""Master hardware test runner. Runs all sensor tests and prints a PASS/FAIL summary."""
import subprocess
import sys
import os
import time

TESTS = [
    ("BMP280   (pressure/temp)",  "test_bmp280.py"),
    ("DHT22    (air temp/hum)",   "test_dht22.py"),
    ("DS18B20  (soil temp)",      "test_ds18b20.py"),
    ("Soil     (moisture %)",     "test_soil.py"),
    ("MQ       (CO + AQI)",       "test_mq.py"),
    ("OLED     (SH1106 display)", "test_oled.py"),
    ("RTC      (DS3231 clock)",   "test_rtc.py"),
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH = 60

print("=" * WIDTH)
print(" HICS IESH — Full Hardware Diagnostic")
print("=" * WIDTH)
print()

results = []

for label, script in TESTS:
    path = os.path.join(SCRIPT_DIR, script)
    print(f"Running: {label}")
    print("-" * WIDTH)
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=False,
            text=True,
            timeout=60
        )
        elapsed = time.time() - start
        passed = result.returncode == 0
        # Parse the last "Result:" line for detail
        status = "PASS" if passed else "FAIL"
    except subprocess.TimeoutExpired:
        elapsed = 60
        status = "TIMEOUT"
        passed = False
    except Exception as e:
        elapsed = 0
        status = f"ERROR: {e}"
        passed = False

    results.append((label, status, elapsed))
    print()
    time.sleep(1)  # let I2C bus settle between tests

print("=" * WIDTH)
print(" SUMMARY")
print("=" * WIDTH)
for label, status, elapsed in results:
    icon = "OK" if status == "PASS" else "!!"
    print(f"  [{icon}] {label:<35}  {status}  ({elapsed:.1f}s)")

total = len(results)
passed = sum(1 for _, s, _ in results if s == "PASS")
print()
print(f"  {passed}/{total} sensors passed")
print("=" * WIDTH)

sys.exit(0 if passed == total else 1)
