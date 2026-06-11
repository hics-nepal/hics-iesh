#!/usr/bin/env python3
"""Bootstrap MQ-7 / MQ-135 clean-air R0 baselines from *existing DB logs*.

Instead of waiting for a live 30-min warm-up, this script uses early-morning
rows already in the database (04:00–08:00 by default — when the room was quiet
and the sensor was running continuously) as a proxy for "cleanest available air".

The resulting mq_cal.json is identical in format to the one written by
calibrate_mq.py — the dashboard and OLED pick it up automatically.

Why 04:00–08:00?
  • The sensor was running continuously during these hours in your room.
  • No cooking, traffic, or other obvious CO/VOC sources.
  • Stable temperature → stable sensor resistance.
  • Not outdoors-clean, but good enough for a *relative* AQI trend indicator.

Usage (run on the Pi or any machine that has DB access):
  python3 scripts/calibrate_mq_from_db.py [options]

Options:
  --night-start HH   Start hour of quiet window (default: 4)
  --night-end   HH   End hour, exclusive (default: 8)
  --days        N    Look back N calendar days (default: 7)
  --min-rows    N    Refuse to calibrate with fewer than N rows (default: 30)
  --dry-run          Print the computed values but don't write mq_cal.json
  --output PATH      Override output path (default: MQ_CAL_PATH from config)

Accuracy note:
  Indoor-air R0 is noisier than a proper outdoor-clean-air R0, so ppm
  readings will carry an extra ±30-50% uncertainty on top of the usual
  sensor tolerances. The proxy AQI is still useful for spotting relative
  trends — "did air quality get worse after cooking?" etc.
"""
import argparse
import json
import math
import os
import sqlite3
import sys
from datetime import datetime, timedelta

# ── Path fix so we can import from the project root ──────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Import config + air_quality via importlib so we bypass sensors/__init__.py
# (which pulls in Pi-only hardware libraries like `board` and `RPi.GPIO`).
import importlib.util as _ilu

def _load_module(rel_path, name):
    spec = _ilu.spec_from_file_location(name, os.path.join(ROOT, rel_path))
    mod  = _ilu.module_from_spec(spec)
    # Register before exec so relative imports inside the module resolve.
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

_cfg = _load_module('sensors/config.py',      'sensors.config')
_aq  = _load_module('sensors/air_quality.py', 'sensors.air_quality')

DB_PATH          = _cfg.DB_PATH
MQ_CAL_PATH      = _cfg.MQ_CAL_PATH
MQ_VCC           = _cfg.MQ_VCC
MQ_RL_OHM        = _cfg.MQ_RL_OHM
MQ_DIVIDER_RATIO = _cfg.MQ_DIVIDER_RATIO

MQ135_A          = _aq.MQ135_A
MQ135_B          = _aq.MQ135_B
CO2_BASELINE_PPM = _aq.CO2_BASELINE_PPM
MQ7_CLEAN_RATIO  = _aq.MQ7_CLEAN_RATIO


# ── RS calculation (mirrors web/app.py _mq_rs) ───────────────────────────────

def raw_to_rs(raw_adc):
    """Convert a stored raw ADC integer → sensor resistance RS (Ω)."""
    if raw_adc is None or raw_adc <= 0:
        return None
    # ADC voltage (after divider correction gives true sensor voltage)
    v_sensor = (raw_adc / 4095.0) * 3.3 * MQ_DIVIDER_RATIO
    if v_sensor < 0.05:          # sensor shorted / disconnected
        return None
    rs = MQ_RL_OHM * (MQ_VCC / v_sensor - 1.0)
    if rs <= 0 or math.isnan(rs) or math.isinf(rs):
        return None
    return rs


# ── Database query ────────────────────────────────────────────────────────────

def fetch_nighttime_rows(days, night_start, night_end):
    """Return list of (mq7_raw, mq135_raw) from nighttime rows in the last N days."""
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()

    # Build the time-of-day filter.  Night windows can wrap midnight
    # (e.g. 22–05), so we need an OR condition.
    if night_start < night_end:
        # e.g. 01:00–06:00 — simple range, no wraparound
        time_filter = (
            "CAST(strftime('%H', timestamp) AS INTEGER) >= ? "
            "AND CAST(strftime('%H', timestamp) AS INTEGER) < ?"
        )
        time_params = (night_start, night_end)
    else:
        # e.g. 22:00–05:00 — wraps midnight
        time_filter = (
            "CAST(strftime('%H', timestamp) AS INTEGER) >= ? "
            "OR CAST(strftime('%H', timestamp) AS INTEGER) < ?"
        )
        time_params = (night_start, night_end)

    sql = f"""
        SELECT mq7_raw, mq135_raw
        FROM   telemetry
        WHERE  timestamp >= ?
          AND  mq7_raw    IS NOT NULL
          AND  mq135_raw  IS NOT NULL
          AND  mq7_raw    > 0
          AND  mq135_raw  > 0
          AND  ({time_filter})
        ORDER  BY timestamp ASC
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(sql, (cutoff, *time_params)).fetchall()
        return rows
    except Exception as e:
        print(f"[DB] Query failed: {e}")
        sys.exit(1)


# ── Outlier trimming (remove top/bottom 10%) ─────────────────────────────────

def trimmed_mean(values, trim=0.10):
    if not values:
        return None
    s = sorted(values)
    cut = max(1, int(len(s) * trim))
    trimmed = s[cut:-cut] if len(s) > 2 * cut else s
    return sum(trimmed) / len(trimmed)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--night-start', type=int, default=4, metavar='HH',
                    help='Start hour of quiet window (default 4 = 04:00)')
    ap.add_argument('--night-end',   type=int, default=8, metavar='HH',
                    help='End hour of quiet window, exclusive (default 8 = 08:00)')
    ap.add_argument('--days',        type=int, default=7,  metavar='N',
                    help='Look back N calendar days (default 7)')
    ap.add_argument('--min-rows',    type=int, default=30, metavar='N',
                    help='Abort if fewer than N nighttime rows found (default 30)')
    ap.add_argument('--dry-run',     action='store_true',
                    help="Compute values but don't write the JSON file")
    ap.add_argument('--output',      default=MQ_CAL_PATH, metavar='PATH',
                    help=f'Output path (default: {MQ_CAL_PATH})')
    args = ap.parse_args()

    print(f"Querying DB: last {args.days} day(s), "
          f"quiet window {args.night_start:02d}:00–{args.night_end:02d}:00 …")
    rows = fetch_nighttime_rows(args.days, args.night_start, args.night_end)

    if len(rows) < args.min_rows:
        print(f"\n✗  Only {len(rows)} qualifying rows found "
              f"(need at least {args.min_rows}).")
        print("   Try --days 14 (look further back) or --min-rows 10 to lower "
              "the threshold.")
        sys.exit(1)

    print(f"Found {len(rows)} nighttime rows — computing RS values …")

    rs7_samples   = [r for r in (raw_to_rs(row[0]) for row in rows) if r is not None]
    rs135_samples = [r for r in (raw_to_rs(row[1]) for row in rows) if r is not None]

    if len(rs7_samples) < args.min_rows // 2 or len(rs135_samples) < args.min_rows // 2:
        print(f"✗  Too many RS=None (ADC saturated or sensor disconnected?).")
        print(f"   rs7 valid={len(rs7_samples)}, rs135 valid={len(rs135_samples)}")
        sys.exit(1)

    rs7_clean   = trimmed_mean(rs7_samples)
    rs135_clean = trimmed_mean(rs135_samples)

    # Derive R0 using the same formulas as calibrate_mq.py ──────────────────
    # MQ-7:   datasheet clean-air ratio  RS_clean / R0 = MQ7_CLEAN_RATIO
    r0_mq7 = rs7_clean / MQ7_CLEAN_RATIO
    # MQ-135: anchor so ppm curve reads atmospheric CO2 (≈420 ppm) in clean air
    r0_mq135 = rs135_clean * (CO2_BASELINE_PPM / MQ135_A) ** (1.0 / MQ135_B)

    # Quick sanity check — wildly wrong R0 usually means ADC wiring problem
    if not (10 < r0_mq7 < 100_000):
        print(f"⚠  r0_mq7={r0_mq7:.0f}Ω looks suspicious — check MQ_RL_OHM "
              f"and MQ_DIVIDER_RATIO in sensors/config.py")
    if not (10 < r0_mq135 < 100_000):
        print(f"⚠  r0_mq135={r0_mq135:.0f}Ω looks suspicious — check config.")

    # ── Report ────────────────────────────────────────────────────────────────
    print()
    print(f"  Rows used    : {len(rs7_samples)} MQ-7 / {len(rs135_samples)} MQ-135")
    print(f"  RS clean-air : MQ-7 {rs7_clean:.0f} Ω   MQ-135 {rs135_clean:.0f} Ω")
    print(f"  Anchored R0  : MQ-7 {r0_mq7:.0f} Ω   MQ-135 {r0_mq135:.0f} Ω")
    print()

    cal = {
        'r0_mq7':           round(r0_mq7, 1),
        'r0_mq135':         round(r0_mq135, 1),
        'rs_clean_mq7':     round(rs7_clean, 1),
        'rs_clean_mq135':   round(rs135_clean, 1),
        'samples':          len(rs7_samples),
        'source':           'db_nighttime_average',
        'night_window':     f'{args.night_start:02d}:00–{args.night_end:02d}:00',
        'lookback_days':    args.days,
        'calibrated_at':    datetime.now().isoformat(timespec='seconds'),
        'note': (
            'R0 derived from DB nighttime average (indoor room air). '
            'ppm readings carry ~±50% uncertainty. '
            'Re-run calibrate_mq.py outdoors for a better baseline.'
        ),
    }

    if args.dry_run:
        print("DRY RUN — would have written:")
        print(json.dumps(cal, indent=2))
        return

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(cal, f, indent=2)

    print(f"✓  Wrote {args.output}")
    print("   Proxy AQI is now live on the dashboard and OLED.")
    print("   TIP: re-run calibrate_mq.py outdoors after 24-48 h burn-in for "
          "a tighter baseline when you get the chance.")


if __name__ == '__main__':
    main()
