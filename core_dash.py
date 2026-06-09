"""HICS Core Dashboard — OLED sensor loop with DB logging and API upload."""
import time
from datetime import datetime

from sensors.dht22 import DHT22
from sensors.bmp280_sensor import BMP280Sensor
from sensors.ds18b20 import DS18B20
from sensors.mcp3208 import MCP3208
from sensors.oled import OLED
from sensors.config import (
    CH_MQ7, CH_MQ135,
    OLED_CYCLE_SECS, DB_LOG_SECS, UPLOAD_SECS
)
import data.database as db
from data.uploader import upload

# ── Hardware Init ──────────────────────────────────────────────────────────────
print("Initializing HICS hardware...")
dht    = DHT22()
bmp    = BMP280Sensor()
ds18   = DS18B20()
adc    = MCP3208()
oled   = OLED()

for name, sensor in [("DHT22", dht), ("BMP280", bmp), ("DS18B20", ds18),
                      ("MCP3208", adc), ("OLED", oled)]:
    status = "OK" if sensor.ok else f"FAIL ({sensor.error})"
    print(f"  {name:<10} {status}")

db.init()

# ── State ──────────────────────────────────────────────────────────────────────
history_temp = []
history_soil = []
air_t = air_h = 0.0
state = 0
last_ui    = time.time()
last_db    = time.time()
last_upload = time.time()

print("Running. Press Ctrl+C to exit.")

try:
    while True:
        # ── Read sensors ──────────────────────────────────────────────────────
        _, pressure   = bmp.read()
        pressure      = pressure or 0.0
        soil_moist    = adc.read_soil_pct()
        mq7_raw       = adc.read_raw(CH_MQ7)
        mq135_raw     = adc.read_raw(CH_MQ135)
        soil_temp     = ds18.read() or 0.0

        new_t, new_h = dht.read()
        if new_t is not None:
            air_t, air_h = new_t, new_h

        history_temp.append(air_t)
        history_soil.append(soil_moist)
        if len(history_temp) > 128: history_temp.pop(0)
        if len(history_soil) > 128: history_soil.pop(0)

        # ── Cycle OLED screen ─────────────────────────────────────────────────
        now = time.time()
        if now - last_ui > OLED_CYCLE_SECS:
            state = (state + 1) % 5
            last_ui = now

        if oled.ok:
            with oled.canvas() as draw:
                if state == 0:
                    draw.text((0,  0), "== HICS CLIMATE ==",   fill="white")
                    draw.text((0, 14), f"Air:  {air_t:.1f}C {air_h:.0f}%", fill="white")
                    draw.text((0, 28), f"Pres: {pressure:.1f} hPa",         fill="white")
                    draw.text((0, 42), f"Soil: {soil_temp:.1f}C {soil_moist:.0f}%", fill="white")
                elif state == 1:
                    draw.text((0,  0), "== AIR QUALITY ==",    fill="white")
                    draw.text((0, 16), f"CO  (MQ7) : {mq7_raw}",   fill="white")
                    draw.text((0, 32), f"AQI(MQ135): {mq135_raw}", fill="white")
                    bar = min(128, int((mq135_raw / 4095) * 128))
                    draw.rectangle((0, 50, bar, 60), fill="white")
                elif state == 2:
                    oled.draw_sparkline(draw, "Air Temp (C)",     history_temp, -10, 40)
                elif state == 3:
                    oled.draw_sparkline(draw, "Soil Moist (%)",   history_soil,   0, 100)
                elif state == 4:
                    ts = datetime.now().strftime("%H:%M:%S")
                    draw.text((0,  0), "== IESH STATUS ==",  fill="white")
                    draw.text((0, 14), f"Time: {ts}",         fill="white")
                    draw.text((0, 28), f"DB logs running",    fill="white")

        # ── Log to SQLite ─────────────────────────────────────────────────────
        if now - last_db > DB_LOG_SECS:
            db.log(air_t, air_h, soil_temp, soil_moist, pressure, mq7_raw, mq135_raw)
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
