#!/usr/bin/env python3
"""Master hardware test runner. Runs all sensor tests and prints a PASS/FAIL summary.

    python3 tests/test_all.py                    # everything
    python3 tests/test_all.py --skip camera      # camera is out (HANDOFF F6)
    python3 tests/test_all.py --only bmp280,oled,rtc   # the I2C trio, bench step 5

Listed in the bench bring-up order of HANDOFF §14 step 5: I2C trio first, then
the ADC and soil, then 1-Wire, then DHT22, then the MQ pair. Add one sensor,
run this, add the next — so an intermittent fault stays attributable.
"""
import subprocess
import sys
import os
import time

TESTS = [  # (key, label, script)
    ("bmp280",  "BMP280   (pressure/temp)",  "test_bmp280.py"),
    ("oled",    "OLED     (SH1106 display)", "test_oled.py"),
    ("rtc",     "RTC      (DS3231 clock)",   "test_rtc.py"),
    ("mcp3208", "MCP3208  (ADC raw)",        "test_mcp3208.py"),
    ("soil",    "Soil     (moisture %)",     "test_soil.py"),
    ("ds18b20", "DS18B20  (soil temp)",      "test_ds18b20.py"),
    ("dht22",   "DHT22    (air temp/hum)",   "test_dht22.py"),
    ("mq",      "MQ       (CO + AQI)",       "test_mq.py"),
    ("camera",  "Camera   (OV5647 sky cam)", "test_camera.py"),
]


def _select(argv):
    keys = [k for k, _, _ in TESTS]
    only, skip = None, set()
    args = list(argv)
    while args:
        a = args.pop(0)
        if a in ('--only', '--skip') and args:
            want = {w.strip().lower() for w in args.pop(0).split(',') if w.strip()}
            bad = want - set(keys)
            if bad:
                sys.exit(f"unknown sensor key(s) {sorted(bad)}; choose from {keys}")
            if a == '--only':
                only = want
            else:
                skip |= want
        else:
            sys.exit(f"usage: test_all.py [--only k1,k2] [--skip k1,k2]   keys: {keys}")
    return [(l, s) for k, l, s in TESTS
            if (only is None or k in only) and k not in skip]


SELECTED = _select(sys.argv[1:])

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH = 60

print("=" * WIDTH)
print(" HICS IESH — Full Hardware Diagnostic")
print("=" * WIDTH)
print()

results = []

for label, script in SELECTED:
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
