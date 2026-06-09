import time
import os
import glob
import board
import adafruit_dht
import smbus2
import spidev
import sqlite3
from datetime import datetime
from bmp280 import BMP280

# Luma OLED Libraries
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

# ==========================================
# 1. HARDWARE INITIALIZATION
# ==========================================
print("Initializing HICS Hardware Array...")

# OLED (I2C Address 0x3C)
try:
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial, width=128, height=64)
except Exception as e:
    print(f"OLED Init Error: {e}")

# BMP280 (I2C Address 0x76)
try:
    bus = smbus2.SMBus(1)
    bmp = BMP280(i2c_dev=bus, i2c_addr=0x76)
except Exception:
    bmp = None

# DHT22 (GPIO 23)
try:
    dht_sensor = adafruit_dht.DHT22(board.D23, use_pulseio=False)
except Exception:
    dht_sensor = None

# SPI Bus (MCP3208)
try:
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    spi_active = True
except Exception:
    spi_active = False

# 1-Wire (DS18B20 on GPIO 4)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
try:
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
except IndexError:
    device_file = None

# ==========================================
# 2. DATABASE INITIALIZATION
# ==========================================
DB_PATH = '/home/pawan/iesh_data_v2.db' 

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Upgraded table to include the new MQ Gas sensors
    c.execute('''CREATE TABLE IF NOT EXISTS telemetry
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME,
                  air_temp REAL, air_hum REAL,
                  soil_temp REAL, soil_moist REAL,
                  pressure REAL,
                  mq7_raw INTEGER, mq135_raw INTEGER)''')
    conn.commit()
    conn.close()

def log_to_db(air_t, air_h, soil_t, soil_m, pres, mq7, mq135):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO telemetry 
                     (timestamp, air_temp, air_hum, soil_temp, soil_moist, pressure, mq7_raw, mq135_raw) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (datetime.now(), air_t, air_h, soil_t, soil_m, pres, mq7, mq135))
        conn.commit()
        conn.close()
    except Exception as e:
        pass

init_db()

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
SOIL_DRY = 4018
SOIL_WET = 2084

def read_mcp3208(channel):
    if not spi_active: return 0
    cmd = [0x06 | (channel >> 2), (channel & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

def read_ds18b20():
    if not device_file: return 0.0
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        if lines[0].strip()[-3:] != 'YES': return 0.0
        temp_string = lines[1].find('t=')
        if temp_string != -1:
            return float(lines[1][temp_string+2:]) / 1000.0
    except Exception:
        return 0.0

def draw_sparkline(draw, title, data_list, max_val, min_val):
    draw.text((0, 0), f"Graph: {title}", fill="white")
    if len(data_list) < 2:
        draw.text((0, 20), "Gathering data...", fill="white")
        return
        
    width = 128
    height = 50
    y_offset = 14
    range_val = max_val - min_val if max_val != min_val else 1
    
    for i in range(1, len(data_list)):
        x1 = int((i - 1) * (width / 128))
        y1 = height + y_offset - int(((data_list[i-1] - min_val) / range_val) * height)
        x2 = int(i * (width / 128))
        y2 = height + y_offset - int(((data_list[i] - min_val) / range_val) * height)
        draw.line((x1, y1, x2, y2), fill="white")

# ==========================================
# 4. MAIN OPERATING LOOP
# ==========================================
print("HICS Core Dash Running. Press Ctrl+C to exit.")

state = 0
last_ui_switch = time.time()
last_db_log = time.time()

history_soil = []
history_temp = []

# Persistent variables so OLED doesn't blink if DHT fails a read
air_t = 0.0
air_h = 0.0

try:
    while True:
        # --- A. Gather Data ---
        pressure = bmp.get_pressure() if bmp else 0.0
        
        mq7_raw = read_mcp3208(0)
        mq135_raw = read_mcp3208(1)
        soil_raw = read_mcp3208(2)
        
        soil_pct = 0
        if SOIL_DRY != SOIL_WET:
            soil_pct = max(0, min(100, ((SOIL_DRY - soil_raw) / (SOIL_DRY - SOIL_WET)) * 100))
        
        soil_temp = read_ds18b20()

        if dht_sensor:
            try:
                air_t = dht_sensor.temperature
                air_h = dht_sensor.humidity
            except RuntimeError:
                pass # Ignore DHT skips

        # Store History for Graphs
        history_soil.append(soil_pct)
        history_temp.append(air_t if air_t else 0)

        if len(history_soil) > 128: history_soil.pop(0)
        if len(history_temp) > 128: history_temp.pop(0)

        # --- B. Cycle OLED UI (Every 4 seconds) ---
        if time.time() - last_ui_switch > 4:
            state = (state + 1) % 4  # Cycles Pages 0, 1, 2, 3
            last_ui_switch = time.time()

        # --- C. Log to SQLite (Every 60 seconds) ---
        if time.time() - last_db_log > 60:
            log_to_db(air_t, air_h, soil_temp, soil_pct, pressure, mq7_raw, mq135_raw)
            last_db_log = time.time()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Data logged to DB.")

        # --- D. Render the OLED ---
        with canvas(device) as draw:
            if state == 0:
                # Main Climate Dash
                draw.text((0, 0),  "== HICS CLIMATE ==", fill="white")
                draw.text((0, 14), f"Air T: {air_t:.1f}C H:{air_h:.0f}%", fill="white")
                draw.text((0, 28), f"Pres : {pressure:.1f} hPa", fill="white")
                draw.text((0, 42), f"SoilT: {soil_temp:.1f}C", fill="white")
            elif state == 1:
                # Gas / AQI Dash
                draw.text((0, 0),  "== AIR QUALITY ==", fill="white")
                draw.text((0, 16), f"CO (MQ7)  : {mq7_raw}", fill="white")
                draw.text((0, 32), f"AQI(MQ135): {mq135_raw}", fill="white")
                # Draw a mini visual bar for AQI
                bar_width = min(128, int((mq135_raw / 4095) * 128))
                draw.rectangle((0, 50, bar_width, 60), fill="white")
            elif state == 2:
                # Sparkline: Temperature
                draw_sparkline(draw, "Air Temp (C)", history_temp, 40, -10)
            elif state == 3:
                # Sparkline: Soil Moisture
                draw_sparkline(draw, "Soil Moist (%)", history_soil, 100, 0)

        time.sleep(1.0) 

except KeyboardInterrupt:
    print("\nShutting down safely...")
    device.clear()
    if dht_sensor: dht_sensor.exit()
    if spi_active: spi.close()
