#!/usr/bin/env python3
"""Calibrate MQ-7 and MQ-135 clean-air baselines (R0).

Run this ON THE PI, ideally:
  - after the sensors have been powered >= 30 min (24-48 h burn-in for new
    sensors gives the most stable baseline)
  - in the cleanest air available (outdoors away from roads/kitchens beats
    indoor air)
  - with a healthy power supply — an undervoltage 5V rail sags the MQ
    heaters and shifts RS, poisoning the baseline

Usage:  python3 scripts/calibrate_mq.py [seconds]   (default 60)

Stop hics-core first if you want exclusive ADC access — not strictly
required (SPI reads interleave fine), but cleaner.

Writes R0 values to MQ_CAL_PATH (~/hics-data/mq_cal.json). The web
dashboard and OLED pick the new calibration up automatically.
"""
import json
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensors.mcp3208 import MCP3208
from sensors.config import CH_MQ7, CH_MQ135, MQ_CAL_PATH
from sensors.air_quality import (
    MQ135_A, MQ135_B, CO2_BASELINE_PPM, MQ7_CLEAN_RATIO,
)


def main():
    secs = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    adc = MCP3208()
    if not adc.ok:
        print(f"ADC init failed: {adc.error}")
        sys.exit(1)

    print(f"Sampling MQ sensors for {secs}s — keep the air around the "
          f"sensors as clean as possible...")
    rs7_samples, rs135_samples = [], []
    for i in range(secs):
        rs7 = adc.read_mq_rs(CH_MQ7)
        rs135 = adc.read_mq_rs(CH_MQ135)
        if rs7:
            rs7_samples.append(rs7)
        if rs135:
            rs135_samples.append(rs135)
        if i % 10 == 0:
            print(f"  {i:3d}s  RS(MQ-7)={rs7 and round(rs7) or '--'}Ω  "
                  f"RS(MQ-135)={rs135 and round(rs135) or '--'}Ω")
        time.sleep(1)

    if len(rs7_samples) < secs // 2 or len(rs135_samples) < secs // 2:
        print("Too many failed reads — check wiring/power and try again.")
        sys.exit(1)

    rs7_clean = sum(rs7_samples) / len(rs7_samples)
    rs135_clean = sum(rs135_samples) / len(rs135_samples)

    # MQ-7: datasheet clean-air ratio anchors R0
    r0_mq7 = rs7_clean / MQ7_CLEAN_RATIO
    # MQ-135: choose R0 so the ppm curve reads atmospheric CO2 right now
    r0_mq135 = rs135_clean * (CO2_BASELINE_PPM / MQ135_A) ** (1 / MQ135_B)

    cal = {
        'r0_mq7':       round(r0_mq7, 1),
        'r0_mq135':     round(r0_mq135, 1),
        'rs_clean_mq7':   round(rs7_clean, 1),
        'rs_clean_mq135': round(rs135_clean, 1),
        'samples':      len(rs135_samples),
        'calibrated_at': datetime.now().isoformat(timespec='seconds'),
    }
    os.makedirs(os.path.dirname(MQ_CAL_PATH), exist_ok=True)
    with open(MQ_CAL_PATH, 'w') as f:
        json.dump(cal, f, indent=2)

    print(f"\nClean-air RS:  MQ-7 {rs7_clean:.0f}Ω   MQ-135 {rs135_clean:.0f}Ω")
    print(f"Anchored R0:   MQ-7 {r0_mq7:.0f}Ω   MQ-135 {r0_mq135:.0f}Ω")
    print(f"Saved to {MQ_CAL_PATH}")
    print("Proxy AQI is now live on the dashboard and OLED.")
    print("TIP: re-run outdoors after 24-48h continuous burn-in (and after "
          "fixing any undervoltage) for a better baseline.")


if __name__ == '__main__':
    main()
