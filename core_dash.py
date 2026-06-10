"""HICS Core Dashboard — OLED sensor loop with DB logging and API upload.

Screens (cycle every OLED_CYCLE_SECS):
  0  Climate:    air temp, humidity, pressure, altitude
  1  Soil:       soil temp, moisture % with bar
  2  Air Quality: CO (MQ-7) and AQI (MQ-135) with bars
  3  Graph:      air temperature sparkline
  4  Graph:      soil moisture sparkline
  5  System:     RTC date/time, WiFi status
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
    OLED_CYCLE_SECS, DB_LOG_SECS, UPLOAD_SECS,
    SEA_LEVEL_HPA,
)
import data.database as db
from data.uploader import upload

SCREENS = 6
HISTORY_LEN = 128


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
history_air_t  = []
history_soil_m = []

air_t      = 0.0
air_h      = 0.0
pressure   = 0.0
altitude   = 0.0
soil_temp  = 0.0
soil_moist = 0.0
mq7_raw    = 0
mq135_raw  = 0

screen       = 0
last_screen  = 0.0
last_db      = time.time()
last_upload  = time.time()
last_wifi_chk= 0.0
wifi_ok      = False
rtc_dt       = None

print("Running. Press Ctrl+C to exit.")

try:
    while True:
        now = time.time()

        # ── Read sensors (non-blocking DHT: 1 attempt, no sleep) ─────────────
        bmp_t, bmp_p = bmp.read()
        if bmp_p:
            pressure = bmp_p
            altitude = pressure_to_altitude(pressure)

        soil_moist = adc.read_soil_pct()
        mq7_raw    = adc.read_raw(CH_MQ7)
        mq135_raw  = adc.read_raw(CH_MQ135)
        _ds = ds18.read()
        if _ds is not None:
            soil_temp = _ds

        new_t, new_h = dht.read(retries=1, delay=0)
        if new_t is not None:
            air_t, air_h = new_t, new_h

        # ── History buffers ───────────────────────────────────────────────────
        for hist, val in [(history_air_t, air_t), (history_soil_m, soil_moist)]:
            hist.append(val)
            if len(hist) > HISTORY_LEN:
                hist.pop(0)

        # ── WiFi check (every 60 s) ───────────────────────────────────────────
        if now - last_wifi_chk > 60:
            wifi_ok = _check_wifi()
            last_wifi_chk = now

        # ── RTC read (once per cycle on system screen, or at startup) ─────────
        if rtc.ok and (rtc_dt is None or now - last_wifi_chk < 2):
            rtc_dt = rtc.read()

        # ── OLED screen cycle ─────────────────────────────────────────────────
        if now - last_screen > OLED_CYCLE_SECS:
            screen = (screen + 1) % SCREENS
            last_screen = now

            # Refresh RTC when entering system screen
            if screen == 5 and rtc.ok:
                rtc_dt = rtc.read()

        if oled.ok:
            ts = (rtc_dt.strftime('%H:%M') if rtc_dt
                  else datetime.now().strftime('%H:%M'))

            with oled.canvas() as draw:

                if screen == 0:
                    draw.text((0,  0), f"CLIMATE     {ts}", fill="white")
                    draw.text((0, 14), f"Air: {air_t:.1f}C  {air_h:.0f}%",
                              fill="white")
                    draw.text((0, 28), f"Pres:{pressure:.1f} hPa", fill="white")
                    draw.text((0, 42), f"Alt: {altitude:.0f} m", fill="white")

                elif screen == 1:
                    draw.text((0,  0), "SOIL MODULE", fill="white")
                    draw.text((0, 14), f"Temp:  {soil_temp:.1f} C", fill="white")
                    draw.text((0, 28), f"Moist: {soil_moist:.0f} %", fill="white")
                    oled.draw_bar(draw, 0, 44, 128, 12, soil_moist / 100)

                elif screen == 2:
                    draw.text((0,  0), "AIR QUALITY", fill="white")
                    draw.text((0, 12), f"CO  MQ-7:  {mq7_raw}", fill="white")
                    oled.draw_bar(draw, 0, 24, 128, 8, mq7_raw / 4095)
                    draw.text((0, 36), f"AQI MQ-135:{mq135_raw}", fill="white")
                    oled.draw_bar(draw, 0, 48, 128, 8, mq135_raw / 4095)

                elif screen == 3:
                    oled.draw_sparkline(draw, "Air Temp (C)", history_air_t)

                elif screen == 4:
                    oled.draw_sparkline(draw, "Soil Moist (%)", history_soil_m,
                                        y_min=0, y_max=100)

                elif screen == 5:
                    date_s = (rtc_dt.strftime('%Y-%m-%d') if rtc_dt
                              else datetime.now().strftime('%Y-%m-%d'))
                    net_s  = "WiFi: OK" if wifi_ok else "WiFi: Offline"
                    draw.text((0,  0), "SYSTEM", fill="white")
                    draw.text((0, 14), date_s, fill="white")
                    draw.text((0, 28), ts,     fill="white")
                    draw.text((0, 42), net_s,  fill="white")

        # ── Log to SQLite ─────────────────────────────────────────────────────
        if now - last_db > DB_LOG_SECS:
            db.log(air_t, air_h, soil_temp, soil_moist, pressure,
                   mq7_raw, mq135_raw)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Logged to DB")
            last_db = now

        # ── Upload to API (when internet available) ───────────────────────────
        if now - last_upload > UPLOAD_SECS:
            row = db.get_latest()
            if row and upload(row):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Uploaded to API")
            last_upload = now

        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nShutting down...")
    oled.clear()
    dht.cleanup()
    adc.cleanup()
