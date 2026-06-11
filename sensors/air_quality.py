"""Proxy AQI estimation from MQ-7 (CO) and MQ-135 (CO2-equivalent) sensors.

IMPORTANT — these are *uncalibrated hobby-grade estimates*, not reference
measurements. The MQ datasheets publish log-log response curves; we fit
ppm = A * (RS/R0)^B and anchor R0 with a clean-air calibration
(scripts/calibrate_mq.py). Accuracy is maybe ±50% at best, and the MQ-7
needs a 5V/1.4V heater cycle for true CO readings which we don't do.
Treat the proxy AQI as a relative trend indicator, good for education
and "is the air getting better or worse", not for health decisions.

Calibration file (~/hics-data/mq_cal.json) is written by
scripts/calibrate_mq.py and reloaded automatically when it changes.
"""
import json
import os
from .config import MQ_CAL_PATH

# Datasheet log-log curve fits: ppm = A * (RS/R0)^B
MQ135_A, MQ135_B = 110.47, -2.862   # CO2-equivalent (GeorgK MQ135 fit)
MQ7_A,   MQ7_B   = 99.042, -1.518   # CO

# R0 anchoring conventions used by calibrate_mq.py:
#   MQ-135: R0 chosen so the curve reads CO2_BASELINE_PPM in clean air
#   MQ-7:   R0 = RS_clean / MQ7_CLEAN_RATIO (datasheet clean-air ratio)
CO2_BASELINE_PPM = 420.0
MQ7_CLEAN_RATIO  = 27.5

# EPA CO sub-index breakpoints (ppm → AQI). Instantaneous proxy for the
# official 8-hour average.
_CO_BP = [(0.0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150),
          (12.5, 15.4, 151, 200), (15.5, 30.4, 201, 300),
          (30.5, 40.4, 301, 400), (40.5, 50.4, 401, 500)]

# CO2-equivalent comfort bands (indoor-air guidance) mapped to AQI scale.
_CO2_BP = [(0, 600, 0, 50), (600, 1000, 51, 100), (1000, 1500, 101, 150),
           (1500, 2000, 151, 200), (2000, 5000, 201, 300),
           (5000, 10000, 301, 500)]

CATEGORIES = [(50, 'Good'), (100, 'Moderate'), (150, 'Sensitive'),
              (200, 'Unhealthy'), (300, 'Very Unhealthy'), (500, 'Hazardous')]
CATEGORIES_SHORT = [(50, 'Good'), (100, 'Mod'), (150, 'USG'),
                    (200, 'Unh'), (300, 'VUnh'), (500, 'Haz')]

_cal = None
_cal_mtime = None


def load_cal():
    """Return {'r0_mq7': Ω, 'r0_mq135': Ω, ...} or None if not calibrated.
    Reloads the file automatically if it changed on disk."""
    global _cal, _cal_mtime
    try:
        mtime = os.path.getmtime(MQ_CAL_PATH)
    except OSError:
        return None
    if _cal is None or mtime != _cal_mtime:
        try:
            with open(MQ_CAL_PATH) as f:
                _cal = json.load(f)
            _cal_mtime = mtime
        except (OSError, ValueError):
            return None
    return _cal


def _ppm(rs, r0, a, b, lo, hi):
    if rs is None or not r0 or rs <= 0:
        return None
    return max(lo, min(hi, a * (rs / r0) ** b))


def co2eq_ppm(rs_mq135):
    cal = load_cal()
    if not cal:
        return None
    return _ppm(rs_mq135, cal.get('r0_mq135'), MQ135_A, MQ135_B, 400, 10000)


def co_ppm(rs_mq7):
    cal = load_cal()
    if not cal:
        return None
    return _ppm(rs_mq7, cal.get('r0_mq7'), MQ7_A, MQ7_B, 0, 1000)


def _subindex(value, breakpoints):
    if value is None:
        return None
    for lo, hi, ilo, ihi in breakpoints:
        if value <= hi:
            if value < lo:
                return ilo
            return round(ilo + (value - lo) * (ihi - ilo) / (hi - lo))
    return 500


def category(aqi, short=False):
    if aqi is None:
        return None
    for limit, name in (CATEGORIES_SHORT if short else CATEGORIES):
        if aqi <= limit:
            return name
    return 'Haz' if short else 'Hazardous'


def proxy_aqi(rs_mq7, rs_mq135):
    """Combined proxy AQI: max of the CO and CO2-eq sub-indices (the same
    'worst pollutant wins' rule the official AQI uses).
    Returns dict or None when uncalibrated."""
    co = co_ppm(rs_mq7)
    co2 = co2eq_ppm(rs_mq135)
    subs = [s for s in (_subindex(co, _CO_BP), _subindex(co2, _CO2_BP))
            if s is not None]
    if not subs:
        return None
    aqi = max(subs)
    return {
        'aqi':        aqi,
        'category':   category(aqi),
        'cat_short':  category(aqi, short=True),
        'co_ppm':     round(co, 1) if co is not None else None,
        'co2eq_ppm':  round(co2) if co2 is not None else None,
    }
