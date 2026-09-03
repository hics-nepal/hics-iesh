"""Channel gating tests — runs anywhere, no hardware needed.

Every case here is a value that was actually found in the station's own
database (see the Sep 2026 diagnosis): the DS18B20's 85.0 reset sentinel,
pressure 0.0, and 416 rows of a bit-identical frozen pressure register. The
point of the suite is that none of them can reach the DB or the website again.

    python3 tests/test_health.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sensors import health   # noqa: E402

CHANNELS = ('air_temp', 'air_hum', 'soil_temp', 'soil_moist',
            'pressure', 'mq7_raw', 'mq135_raw')

_failures = []


def check(desc, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {desc}")
    if not ok:
        print(f"          got {got!r}, want {want!r}")
        _failures.append(desc)


def test_rejects_values_found_in_the_live_db():
    print("rejects the garbage that reached production:")
    c = health.Channel('soil_temp')
    c.update(85.0)          # DS18B20 power-on-reset scratchpad value
    check("DS18B20 85.0 sentinel logs NULL", c.for_log(), None)

    c = health.Channel('pressure')
    c.update(0.0)           # BMP280 absent, v0.1 logged its 0.0 initialiser
    check("pressure 0.0 logs NULL", c.for_log(), None)

    c = health.Channel('air_hum')
    check("a sensor that never read logs NULL, not 0.0", c.for_log(), None)


def test_keeps_real_readings():
    print("keeps real readings:")
    c = health.Channel('pressure')
    c.update(869.8, raw=412345)   # plausible for Lalitpur at ~1350 m
    check("869.8 hPa kept", c.for_log(), 869.8)

    c = health.Channel('soil_temp')
    c.update(25.625)
    check("soil 25.625 C kept", c.for_log(), 25.625)

    c = health.Channel('mq7_raw')
    c.update(4095)
    check("ADC full scale kept", c.for_log(), 4095)


def test_frozen_register():
    print("frozen register:")
    c = health.Channel('pressure')
    for _ in range(health.FROZEN_REPEATS + 5):
        c.update(800.647395954495, raw=333333)
    check("bit-identical repeats log NULL", c.for_log(), None)
    check("state reports 'frozen'", c.state, 'frozen')

    c.update(869.9, raw=444444)
    check("recovers once the register moves", c.for_log(), 869.9)
    check("state back to 'ok'", c.state, 'ok')

    # A steady real sensor still dithers in the low bits — must not be flagged.
    c = health.Channel('pressure')
    for i in range(40):
        c.update(869.0 + i * 0.01, raw=400000 + i)
    check("dithering sensor is not called frozen", c.state, 'ok')


def test_staleness():
    print("staleness:")
    c = health.Channel('air_temp', max_age=0.05)
    c.update(25.4)
    check("fresh reading kept", c.for_log(), 25.4)
    time.sleep(0.08)
    check("past max_age logs NULL", c.for_log(), None)
    check("state reports 'stale'", c.state, 'stale')

    c = health.Channel('air_temp')
    c.update(25.4)
    c.update(None)     # a failed read must not destroy a good recent value
    check("failed read keeps the last good value", c.for_log(), 25.4)

    c = health.Channel('air_hum')
    c.update(50.0)
    c.update(150.0)    # implausible: treated exactly like a failed read
    check("out-of-range rejected, previous kept", c.for_log(), 50.0)


def test_channelset_row_matches_db_signature():
    print("ChannelSet row ordering:")
    cs = health.ChannelSet(CHANNELS)
    cs.update('air_temp', 25.4)
    cs.update('soil_temp', 85.0)     # rejected
    cs.update('pressure', 0.0)       # rejected
    cs.update('mq7_raw', 186)
    check("row() gates each channel independently",
          cs.row(CHANNELS),
          [25.4, None, None, None, None, 186, None])
    check("unhealthy() names every bad channel",
          sorted(cs.unhealthy()),
          ['air_hum', 'mq135_raw', 'pressure', 'soil_moist', 'soil_temp'])

    # Plausible value per channel — a flat 10.0 across the board would be
    # correctly rejected for pressure (below the 300 hPa floor).
    plausible = {'air_temp': 21.5, 'air_hum': 62.0, 'soil_temp': 19.0,
                 'soil_moist': 34.0, 'pressure': 869.4,
                 'mq7_raw': 186, 'mq135_raw': 104}
    cs = health.ChannelSet(CHANNELS)
    for name, value in plausible.items():
        cs.update(name, value)
    check("all-good set reports no unhealthy channels", cs.unhealthy(), {})
    check("summary() says so", cs.summary(), 'all channels ok')


if __name__ == '__main__':
    for fn in (test_rejects_values_found_in_the_live_db,
               test_keeps_real_readings,
               test_frozen_register,
               test_staleness,
               test_channelset_row_matches_db_signature):
        fn()
    print()
    if _failures:
        print(f"{len(_failures)} FAILED: {_failures}")
        sys.exit(1)
    print("all channel-gating tests passed")
