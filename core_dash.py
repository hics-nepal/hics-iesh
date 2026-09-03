"""HICS Core Dashboard — OLED sensor loop with DB logging and API upload.

Screens (cycled; "n/6" page indicator top-right). Organized to mirror
the learn modules — Climate, Soil, Air Quality, Environment, Data:
  0  Summary:  all key values at a glance + time + WiFi    (10 s)
  1  Climate:  air temp, humidity, pressure, altitude       (8 s)
  2  Soil:     soil temp, moisture % with bar               (8 s)
  3  Air:      CO (MQ-7) and AQI (MQ-135) with bars         (8 s)
  4  Trend:    1-hour change rates + weather hint from
               barometric pressure (falling = rain)        (10 s)
  5  System:   date, WiFi, uptime, DB row count             (6 s)
"""
import time
import socket
from datetime import datetime

from sensors.dht22 import DHT22
from sensors.bmp280_sensor import BMP280Sensor
from sensors.ds18b20 import DS18B20
from sensors.mcp3208 import MCP3208
from sensors.oled import OLED
from sensors.rtc import RTC
from sensors.config import (
    CH_MQ7, CH_MQ135,
    DB_LOG_SECS, UPLOAD_SECS,
    SEA_LEVEL_HPA,
)
import data.database as db
from data.uploader import upload_unsynced
from sensors import air_quality as aq
from sensors import health

SCREENS = 6
# Seconds each screen stays visible before cycling to the next.
SCREEN_DURATIONS = [10, 8, 8, 8, 10, 6]

# DB column order — must match data.database.log()'s signature.
CHANNELS = ('air_temp', 'air_hum', 'soil_temp', 'soil_moist',
            'pressure', 'mq7_raw', 'mq135_raw')

# How often to retry a sensor that is currently down. The I2C/1-Wire parts on
# this station drop off their bus under undervoltage and come back; v0.1
# latched ok=False at init, so one dropout killed a channel until the service
# was restarted by hand.
RECOVER_SECS = 60


def pressure_to_altitude(pressure_hpa):
    """Barometric formula. Accurate to ~±10 m below 3000 m."""
    return 44330.0 * (1.0 - (pressure_hpa / SEA_LEVEL_HPA) ** 0.1903)


def _check_wifi():
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect(('8.8.8.8', 53))
        s.close()
        return True
    except Exception:
        return False


def _compute_trend():
    """Per-hour change rates from the last hour of logged telemetry.
    Returns None until ~12 min of data exists (rates would be noise)."""
    rows = db.get_recent_hours(1)
    if len(rows) < 5:
        return None
    old, new = rows[0], rows[-1]
    try:
        t0 = datetime.fromisoformat(old['timestamp'])
        t1 = datetime.fromisoformat(new['timestamp'])
    except (KeyError, TypeError, ValueError):
        return None
    span_h = (t1 - t0).total_seconds() / 3600
    if span_h < 0.2:
        return None

    def rate(key):
        a, b = old.get(key), new.get(key)
        if a is None or b is None:
            return None
        return (b - a) / span_h

    dp = rate('pressure')
    # Barometric rule of thumb: pressure falling >0.5 hPa/h hints at rain,
    # rising means clearing. (Ties into the Climate learn module.)
    if dp is None:
        hint = "Gathering..."
    elif dp <= -1.5:
        hint = "Storm coming?"
    elif dp <= -0.5:
        hint = "Rain possible"
    elif dp >= 0.5:
        hint = "Clearing skies"
    else:
        hint = "Steady weather"
    return {'dt': rate('air_temp'), 'dh': rate('air_hum'),
            'dp': dp, 'hint': hint}


# ── Hardware Init ─────────────────────────────────────────────────────────────
print("Initializing HICS hardware...")
dht  = DHT22()
bmp  = BMP280Sensor()
ds18 = DS18B20()
adc  = MCP3208()
rtc  = RTC()
oled = OLED()

for name, sensor in [("DHT22", dht), ("BMP280", bmp), ("DS18B20", ds18),
                      ("MCP3208", adc), ("RTC", rtc), ("OLED", oled)]:
    status = "OK" if sensor.ok else f"FAIL ({sensor.error})"
    print(f"  {name:<10} {status}")

db.init()

# ── State ─────────────────────────────────────────────────────────────────────
# Every logged quantity goes through a health.Channel, which returns None to the
# logger unless the reading is both fresh and physically plausible. v0.1 kept
# these as plain floats initialised to 0.0 and overwrote them only on success,
# so a dead sensor logged 0.0 (or its last good value) forever — 441 rows of
# soil_temp 0.0, 15 of the DS18B20's 85.0 reset sentinel, and 416 rows of
# bit-identical frozen pressure reached the website that way.
ch = health.ChannelSet(CHANNELS)

# Display mirrors of the gated channels, refreshed each loop from `ch`.
air_t      = 0.0
air_h      = 0.0
pressure   = 0.0
altitude   = 0.0
soil_temp  = 0.0
soil_moist = 0.0
mq7_raw    = 0
mq135_raw  = 0
db_rows    = db.count()
last_recover = 0.0

screen        = 0
last_screen   = 0.0
last_db       = time.time()
last_upload   = time.time()
last_wifi_chk = 0.0
wifi_ok       = False
rtc_dt        = None
trend         = _compute_trend()
start_t       = time.time()
last_dht      = 0.0
aqi_info      = None
last_aqi      = 0.0

print("Running. Press Ctrl+C to exit.")

try:
    while True:
        now = time.time()

        # ── Read sensors (non-blocking DHT: 1 attempt, no sleep) ─────────────
        bmp_t, bmp_p = bmp.read()
        # Pass the uncompensated pressure word so the channel can spot a frozen
        # register: a chip that browned out into sleep keeps returning a
        # perfectly plausible — but bit-identical — number.
        ch.update('pressure', bmp_p, raw=bmp.last_raw_p)
        # BMP280 also gives temperature — fallback when DHT22 has no fresh
        # reading. Keyed on channel freshness, not on air_t == 0.0, which
        # misfired at exactly 0 C.
        if bmp_t is not None and not ch['air_temp'].fresh:
            ch.update('air_temp', round(bmp_t, 1))
            # Note: BMP280 has no humidity sensor — air_hum simply ages out.

        ch.update('soil_moist', adc.read_soil_pct())
        ch.update('mq7_raw',   adc.read_raw(CH_MQ7))
        ch.update('mq135_raw', adc.read_raw(CH_MQ135))

        # Proxy AQI (None until scripts/calibrate_mq.py has been run)
        if now - last_aqi >= 10:
            last_aqi = now
            aqi_info = aq.proxy_aqi(adc.read_mq_rs(CH_MQ7),
                                    adc.read_mq_rs(CH_MQ135))
        ch.update('soil_temp', ds18.read())

        # DHT22 requires >= 2 s between reads — poll every 3 s, not every loop
        if now - last_dht >= 3:
            last_dht = now
            new_t, new_h = dht.read(retries=1, delay=0)
            ch.update('air_temp', new_t)
            ch.update('air_hum',  new_h)

        # ── Recover downed sensors (every RECOVER_SECS) ───────────────────────
        if now - last_recover >= RECOVER_SECS:
            last_recover = now
            if not bmp.ok:
                bmp.reinit()
            if not oled.ok:
                oled.reinit()
            # DS18B20 rescans the 1-Wire bus inside read(); MCP3208 is SPI and
            # has no addressing to lose.

        # ── Refresh display mirrors from the gated channels ───────────────────
        air_t      = ch['air_temp'].for_display()
        air_h      = ch['air_hum'].for_display()
        soil_temp  = ch['soil_temp'].for_display()
        soil_moist = ch['soil_moist'].for_display()
        mq7_raw    = int(ch['mq7_raw'].for_display(0))
        mq135_raw  = int(ch['mq135_raw'].for_display(0))
        _p         = ch['pressure'].for_log()
        # Altitude is meaningless without a real pressure — v0.1 fed 0.0 hPa
        # into the barometric formula and displayed 44330 m.
        pressure   = _p if _p is not None else 0.0
        altitude   = pressure_to_altitude(_p) if _p else 0.0


        # ── WiFi check (every 60 s) ───────────────────────────────────────────
        if now - last_wifi_chk > 60:
            wifi_ok = _check_wifi()
            last_wifi_chk = now

        # ── RTC read (once per cycle on system screen, or at startup) ─────────
        if rtc.ok and (rtc_dt is None or now - last_wifi_chk < 2):
            rtc_dt = rtc.read()

        # ── OLED screen cycle ─────────────────────────────────────────────────
        if now - last_screen > SCREEN_DURATIONS[screen]:
            screen = (screen + 1) % SCREENS
            last_screen = now

            # Refresh RTC when entering system screen
            if screen == 5 and rtc.ok:
                rtc_dt = rtc.read()

        # Redraw every loop: the driver diffs pages, so only rows whose
        # values actually changed get rewritten — no visible sweep.
        if oled.ok:
            ts = (rtc_dt.strftime('%H:%M') if rtc_dt
                  else datetime.now().strftime('%H:%M'))

            with oled.canvas() as draw:

                if screen == 0:   # ── Summary ──────────────────────────────
                    wifi_s = "W" if wifi_ok else "!"
                    draw.text((0,  0), f"HICS {ts} {wifi_s}", fill="white")
                    draw.text((0, 14), f"T:{air_t:.1f}C   H:{air_h:.0f}%",
                              fill="white")
                    draw.text((0, 28), f"Sm:{soil_moist:.0f}%  P:{pressure:.0f}",
                              fill="white")
                    draw.text((0, 42), f"CO:{mq7_raw}  AQ:{mq135_raw}",
                              fill="white")

                elif screen == 1:  # ── Climate ──────────────────────────────
                    draw.text((0,  0), f"CLIMATE  {ts}", fill="white")
                    draw.text((0, 14), f"T:{air_t:.1f}C   H:{air_h:.0f}%",
                              fill="white")
                    draw.text((0, 28), f"Pres: {pressure:.1f} hPa", fill="white")
                    draw.text((0, 42), f"Alt:  {altitude:.0f} m", fill="white")

                elif screen == 2:  # ── Soil ─────────────────────────────────
                    draw.text((0,  0), f"SOIL  {ts}", fill="white")
                    draw.text((0, 14), f"Temp:  {soil_temp:.1f} C", fill="white")
                    draw.text((0, 28), f"Moist: {soil_moist:.0f} %", fill="white")
                    oled.draw_bar(draw, 0, 44, 128, 12, soil_moist / 100)

                elif screen == 3:  # ── Air Quality ───────────────────────────
                    draw.text((0,  0), f"AIR QUAL  {ts}", fill="white")
                    if aqi_info:
                        draw.text((0, 14),
                                  f"AQI~{aqi_info['aqi']} {aqi_info['cat_short']}",
                                  fill="white")
                        oled.draw_bar(draw, 0, 27, 128, 7,
                                      aqi_info['aqi'] / 300)
                        draw.text((0, 37),
                                  f"CO~{aqi_info['co_ppm']}  "
                                  f"CO2~{aqi_info['co2eq_ppm']}",
                                  fill="white")
                        draw.text((0, 51), f"raw {mq7_raw}/{mq135_raw}",
                                  fill="white")
                    else:
                        draw.text((0, 14), f"CO  MQ-7:  {mq7_raw}", fill="white")
                        oled.draw_bar(draw, 0, 27, 128, 7, mq7_raw / 4095)
                        draw.text((0, 37), f"AQI MQ-135:{mq135_raw}", fill="white")
                        oled.draw_bar(draw, 0, 51, 128, 7, mq135_raw / 4095)

                elif screen == 4:  # ── Trend / Environment ──────────────────
                    draw.text((0,  0), f"TREND 1h  {ts}", fill="white")
                    if trend:
                        dt_s = (f"{trend['dt']:+.1f}"
                                if trend['dt'] is not None else "--")
                        dh_s = (f"{trend['dh']:+.0f}"
                                if trend['dh'] is not None else "--")
                        dp_s = (f"{trend['dp']:+.1f}"
                                if trend['dp'] is not None else "--")
                        draw.text((0, 14), f"T:{air_t:.1f}C  {dt_s}/h",
                                  fill="white")
                        draw.text((0, 28), f"H:{air_h:.0f}%{dh_s}  P{dp_s}/h",
                                  fill="white")
                        draw.text((0, 42), f"=> {trend['hint']}", fill="white")
                    else:
                        draw.text((0, 14), "Gathering data...", fill="white")
                        draw.text((0, 28), "Need ~15 min of", fill="white")
                        draw.text((0, 42), "readings first.", fill="white")

                elif screen == 5:  # ── System ───────────────────────────────
                    date_s = (rtc_dt.strftime('%Y-%m-%d') if rtc_dt
                              else datetime.now().strftime('%Y-%m-%d'))
                    net_s  = "WiFi:OK" if wifi_ok else "WiFi:--"
                    up = now - start_t
                    up_s = f"{int(up // 3600)}h{int(up % 3600 // 60):02d}m"
                    draw.text((0,  0), f"SYSTEM  {ts}", fill="white")
                    draw.text((0, 14), date_s, fill="white")
                    draw.text((0, 28), f"{net_s}  Up:{up_s}", fill="white")
                    bad = ch.unhealthy()
                    if bad:
                        # Name the failing channels: a silent dead sensor is how
                        # v0.1 logged 46% garbage without anyone noticing.
                        draw.text((0, 42), "BAD:" + ",".join(sorted(bad))[:20],
                                  fill="white")
                    else:
                        draw.text((0, 42), f"DB: {db_rows} rows  OK", fill="white")

                # ── Shared chrome: page indicator top-right ──────────────────
                draw.text((110, 0), f"{screen + 1}/{SCREENS}", fill="white")

        # ── Log to SQLite ─────────────────────────────────────────────────────
        if now - last_db > DB_LOG_SECS:
            db.log(*ch.row(CHANNELS))
            db_rows = db.count()
            trend   = _compute_trend()
            stamp   = datetime.now().strftime('%H:%M:%S')
            bad     = ch.unhealthy()
            note    = f" | NULL: {ch.summary()}" if bad else ""
            print(f"[{stamp}] Logged to DB ({db_rows} rows){note}")
            last_db = now

        # ── Upload to API (when internet available) ───────────────────────────
        if now - last_upload > UPLOAD_SECS:
            n = upload_unsynced()
            if n:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Uploaded {n} row(s) to API")
            last_upload = now

        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nShutting down...")
    oled.clear()
    dht.cleanup()
    adc.cleanup()
