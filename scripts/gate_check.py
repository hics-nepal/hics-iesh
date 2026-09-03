#!/usr/bin/env python3
"""The HANDOFF §14 commissioning gates, as one command run ON THE STATION.

    python3 scripts/gate_check.py            # everything below
    python3 scripts/gate_check.py --json     # machine-readable

Each line is a gate from the build order. PASS means proceed; FAIL means the
next step is not meaningful yet. No sudo needed: the RTC is read through sysfs,
the I2C scan uses smbus2, and the journal is read if the user may (else skipped).

  G1  power      vcgencmd get_throttled == 0x0 (§14 step 1, fault F1)
  G2  config     §11 lines present in config.txt
  G3  rtc        /dev/rtc0 exists and agrees with the system clock (F4)
  G4  i2c        OLED 0x3C, DS3231 0x68 (+0x57 EEPROM), BMP280 0x76 answer
  G5  1-wire     a 28-* probe is on the bus
  G6  services   hics-core + hics-web active; log shows the '| NULL:' note
                 (its ABSENCE means v0.1 is still what is running — §14 step 4)
  G7  data       rows/day for the last days; a full day is 1440 (F5)
"""
import glob
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sensors.config import DB_PATH, I2C_BUS, BMP280_ADDR, OLED_ADDR, RTC_ADDR  # noqa: E402

RESULTS = []


def gate(key, status, detail):
    RESULTS.append((key, status, detail))


def sh(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except (OSError, subprocess.SubprocessError) as e:
        return 1, str(e)


# ── G1 power ─────────────────────────────────────────────────────────────────
THROTTLE_BITS = {
    0: 'under-voltage NOW', 1: 'arm freq capped NOW', 2: 'THROTTLED NOW',
    3: 'soft temp limit NOW', 16: 'under-voltage occurred', 17: 'freq cap occurred',
    18: 'throttling occurred', 19: 'soft temp limit occurred',
}


def g1_power():
    rc, out = sh('vcgencmd get_throttled')
    m = re.search(r'0x([0-9a-fA-F]+)', out)
    if rc or not m:
        return gate('G1 power', 'SKIP', f'vcgencmd unavailable: {out[:60]}')
    v = int(m.group(1), 16)
    flags = [n for b, n in THROTTLE_BITS.items() if v & (1 << b)]
    live = v & 0xF
    if v == 0:
        gate('G1 power', 'PASS', '0x0 - no under-voltage, ever, since boot')
    elif live:
        gate('G1 power', 'FAIL', f'0x{v:x}: ' + ', '.join(flags)
             + '  -> fix the supply/cable (§8) before anything else')
    else:
        gate('G1 power', 'WARN', f'0x{v:x}: ' + ', '.join(flags)
             + '  (history only - was it the MQ heaters switching on?)')
    rc, out = sh('vcgencmd measure_volts core')
    if not rc:
        gate('G1 volts', 'INFO', out + '   (core, not the 5 V rail - meter pins 2/6 for that)')


# ── G2 config ────────────────────────────────────────────────────────────────
def g2_config():
    cfg = '/boot/firmware/config.txt'
    if not os.path.exists(cfg):
        cfg = '/boot/config.txt'
    try:
        lines = [l.strip() for l in open(cfg)]
    except OSError as e:
        return gate('G2 config', 'SKIP', str(e))
    active = [l for l in lines if l and not l.startswith('#')]
    want = {
        'i2c 100 kHz (§11.1)': 'dtparam=i2c_arm_baudrate=100000',
        'rtc overlay (§11.2)': 'dtoverlay=i2c-rtc,ds3231',
        'w1-gpio':             'dtoverlay=w1-gpio',
        'spi on':              'dtparam=spi=on',
    }
    missing = [k for k, v in want.items() if not any(a.startswith(v) for a in active)]
    stray = [a for a in active if a.startswith('dtoverlay=ov5647')]
    if not missing and not stray:
        gate('G2 config', 'PASS', f'{cfg}: all §11 lines present')
    else:
        msg = []
        if missing:
            msg.append('missing ' + ', '.join(missing))
        if stray:
            msg.append('dtoverlay=ov5647 still active (§11.3)')
        gate('G2 config', 'FAIL', '; '.join(msg) + '  -> sudo scripts/pi_config.sh')


# ── G3 rtc ───────────────────────────────────────────────────────────────────
def g3_rtc():
    if not os.path.exists('/dev/rtc0'):
        return gate('G3 rtc', 'FAIL', 'no /dev/rtc0 - overlay not loaded (reboot after pi_config.sh?)')
    try:
        d = open('/sys/class/rtc/rtc0/date').read().strip()
        t = open('/sys/class/rtc/rtc0/time').read().strip()
        rtc = datetime.strptime(f'{d} {t}', '%Y-%m-%d %H:%M:%S')
    except (OSError, ValueError) as e:
        return gate('G3 rtc', 'FAIL', f'/dev/rtc0 exists but unreadable: {e}')
    # sysfs reports the RTC in UTC; compare against UTC system time
    drift = abs((datetime.now(timezone.utc).replace(tzinfo=None) - rtc).total_seconds())
    if rtc.year < 2024:
        gate('G3 rtc', 'FAIL', f'RTC reads {rtc} UTC - never set / coin cell flat. '
             'Fit a fresh CR2032 then: sudo hwclock -w')
    elif drift > 120:
        gate('G3 rtc', 'WARN', f'RTC {rtc} UTC is {drift:.0f} s from system time - sudo hwclock -w')
    else:
        gate('G3 rtc', 'PASS', f'{rtc} UTC, within {drift:.0f} s of system time')


# ── G4 i2c ───────────────────────────────────────────────────────────────────
def g4_i2c():
    try:
        import smbus2
    except ImportError:
        return gate('G4 i2c', 'SKIP', 'smbus2 not installed')
    expect = {OLED_ADDR: 'OLED', RTC_ADDR: 'DS3231', 0x57: 'DS3231 EEPROM', BMP280_ADDR: 'BMP280'}
    found = []
    try:
        bus = smbus2.SMBus(I2C_BUS)
        for a in range(0x03, 0x78):
            try:
                bus.read_byte(a)
                found.append(a)
            except OSError:
                pass
        bus.close()
    except OSError as e:
        return gate('G4 i2c', 'FAIL', f'bus {I2C_BUS} unopenable: {e}')
    names = ', '.join(f'0x{a:02x} {expect.get(a, "?")}' for a in found) or 'nothing'
    missing = [f'0x{a:02x} {n}' for a, n in expect.items() if a not in found]
    if not missing:
        gate('G4 i2c', 'PASS', names)
    elif missing == [f'0x{BMP280_ADDR:02x} BMP280']:
        gate('G4 i2c', 'WARN', f'{names};  BMP280 absent (U7: reconnect, no spare)')
    else:
        gate('G4 i2c', 'FAIL', f'{names};  missing {", ".join(missing)}')


# ── G5 1-wire ────────────────────────────────────────────────────────────────
def g5_w1():
    devs = sorted(os.path.basename(p) for p in glob.glob('/sys/bus/w1/devices/28-*'))
    if not devs:
        return gate('G5 1-wire', 'FAIL', 'no 28-* probe on GPIO4 - check R1 4k7 pull-up and the soil cable')
    # a second read a few seconds later catches the drop-off/return pattern of F2
    time.sleep(3)
    again = sorted(os.path.basename(p) for p in glob.glob('/sys/bus/w1/devices/28-*'))
    if again != devs:
        return gate('G5 1-wire', 'FAIL', f'probe list changed within 3 s ({devs} -> {again}) - F2 is live')
    try:
        raw = open(f'/sys/bus/w1/devices/{devs[0]}/w1_slave').read()
        crc = 'YES' in raw.splitlines()[0]
        t = int(raw.split('t=')[1]) / 1000.0
        if not crc:
            return gate('G5 1-wire', 'FAIL', f'{devs[0]} present but CRC bad - bus marginal')
        if t == 85.0:
            return gate('G5 1-wire', 'FAIL', f'{devs[0]} reads 85.0 = power-on-reset sentinel - supply')
        gate('G5 1-wire', 'PASS', f'{devs[0]}  {t:.3f} C, CRC ok')
    except (OSError, ValueError, IndexError) as e:
        gate('G5 1-wire', 'FAIL', f'{devs[0]} present but unreadable: {e}')


# ── G6 services ──────────────────────────────────────────────────────────────
def g6_services():
    rc, out = sh('systemctl is-active hics-core hics-web')
    states = out.split()
    if states == ['active', 'active']:
        gate('G6 services', 'PASS', 'hics-core + hics-web active')
    else:
        gate('G6 services', 'FAIL', f'hics-core/hics-web = {states or out[:60]}')
    rc, out = sh('journalctl -u hics-core -n 40 --no-pager -o cat 2>/dev/null')
    if rc or not out:
        return gate('G6 log', 'SKIP', 'journal not readable as this user - '
                    'sudo journalctl -u hics-core -n 20')
    logged = [l for l in out.splitlines() if 'Logged to DB' in l]
    if not logged:
        return gate('G6 log', 'WARN', 'no "Logged to DB" line in the last 40 - just restarted?')
    last = logged[-1]
    if '| NULL:' in last or 'all channels ok' in last:
        gate('G6 log', 'PASS', 'v0.2 gating is running:  ' + last[-90:])
    else:
        gate('G6 log', 'WARN', 'log has no "| NULL:" note - v0.1 may still be running; '
             'sudo systemctl restart hics-core hics-web')


# ── G7 data ──────────────────────────────────────────────────────────────────
def g7_data():
    if not os.path.exists(DB_PATH):
        return gate('G7 data', 'FAIL', f'{DB_PATH} does not exist')
    try:
        con = sqlite3.connect(DB_PATH)
        days = con.execute("SELECT date(timestamp) d, COUNT(*) FROM telemetry "
                           "GROUP BY d ORDER BY d DESC LIMIT 5").fetchall()
        today = datetime.now().strftime('%Y-%m-%d')
        cols = ['air_temp', 'air_hum', 'soil_temp', 'soil_moist', 'pressure', 'mq7_raw', 'mq135_raw']
        nulls = con.execute(
            'SELECT ' + ', '.join(f'SUM({c} IS NULL)' for c in cols) + ', COUNT(*) '
            'FROM telemetry WHERE date(timestamp)=?', (today,)).fetchone()
        con.close()
    except sqlite3.Error as e:
        return gate('G7 data', 'FAIL', f'sqlite: {e}')
    if not days:
        return gate('G7 data', 'WARN', 'no rows yet')
    per_day = '  '.join(f'{d}:{n}' for d, n in days)
    full = [d for d, n in days if n >= 1400]
    status = 'PASS' if full else 'WARN'
    gate('G7 data', status, f'rows/day  {per_day}   (full day = 1440; F5 closes on the first)')
    n = nulls[-1]
    if n:
        frac = ', '.join(f'{c} {100 * (v or 0) / n:.0f}%' for c, v in zip(cols, nulls[:-1]) if v)
        gate('G7 nulls', 'INFO', f'today: {n} rows; NULL share  {frac or "none"}')


def main():
    for fn in (g1_power, g2_config, g3_rtc, g4_i2c, g5_w1, g6_services, g7_data):
        try:
            fn()
        except Exception as e:      # a gate must never take the others down
            gate(fn.__name__, 'SKIP', f'{type(e).__name__}: {e}')
    if '--json' in sys.argv:
        print(json.dumps([dict(gate=k, status=s, detail=d) for k, s, d in RESULTS], indent=1))
    else:
        print(f'HICS IESH gate check  {datetime.now():%Y-%m-%d %H:%M}  ({os.uname().nodename})')
        print('-' * 78)
        for k, s, d in RESULTS:
            print(f'{s:<5} {k:<12} {d}')
        print('-' * 78)
        fails = [k for k, s, _ in RESULTS if s == 'FAIL']
        print('NOT READY: ' + ', '.join(fails) if fails else 'all gates pass')
    sys.exit(1 if any(s == 'FAIL' for _, s, _ in RESULTS) else 0)


if __name__ == '__main__':
    main()
