import time
import os
import glob
import board
import adafruit_dht
import smbus2
import spidev
from bmp280 import BMP280
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

# --- Hardware Initialization ---
serial = i2c(port=1, address=0x3C)
device = sh1106(serial, width=128, height=64)

# DHT22 on Pin 16 (GPIO 23)
dht_sensor = adafruit_dht.DHT22(board.D23)

# BMP280 on I2C
bus = smbus2.SMBus(1)
RTC_ADDRESS = 0x68
bmp = BMP280(i2c_dev=bus)

# MCP3208 on SPI (CE0)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
SOIL_DRY = 4018
SOIL_WET = 2084

# --- 1-Wire DS18B20 Setup ---
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
try:
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
except IndexError:
    device_file = None

history_soil = []
history_temp = []

def read_ds18b20():
    if not device_file:
        return None
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        if lines[0].strip()[-3:] != 'YES':
            return None
        temp_string = lines[1].find('t=')
        if temp_string != -1:
            temp_data = lines[1][temp_string+2:]
            return float(temp_data) / 1000.0
    except Exception:
        return None

def read_mcp3208(channel):
    cmd = [0x06 | (channel >> 2), (channel & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

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

print("Starting Unified Dashboard... Press Ctrl+C to stop.")

state = 0
last_switch = time.time()

try:
    while True:
        pressure = bmp.get_pressure()
        raw_soil = read_mcp3208(0)
        soil_pct = max(0, min(100, ((SOIL_DRY - raw_soil) / (SOIL_DRY - SOIL_WET)) * 100))
        soil_temp = read_ds18b20()
        soil_temp_str = f"{soil_temp:.1f}C" if soil_temp else "N/A"

        try:
            air_t = dht_sensor.temperature
            air_h = dht_sensor.humidity
            dht_str = f"Air: {air_t:.1f}C | {air_h:.1f}%" if air_t else "Air: Wait..."
            if air_t:
                history_temp.append(air_t)
        except RuntimeError:
            dht_str = "Air: Wait..."

        history_soil.append(soil_pct)

        if len(history_soil) > 128: history_soil.pop(0)
        if len(history_temp) > 128: history_temp.pop(0)

        if time.time() - last_switch > 5:
            state = (state + 1) % 3
            last_switch = time.time()

        with canvas(device) as draw:
            if state == 0:
                draw.text((0, 0),  "=== IESH LIVE ===", fill="white")
                draw.text((0, 13), dht_str, fill="white")
                draw.text((0, 26), f"Pres:  {pressure:.0f} hPa", fill="white")
                draw.text((0, 39), f"S-Hum: {soil_pct:.1f}%", fill="white")
                draw.text((0, 52), f"S-Tmp: {soil_temp_str}", fill="white")
            elif state == 1:
                draw_sparkline(draw, "Soil Moist (%)", history_soil, 100, 0)
            elif state == 2:
                draw_sparkline(draw, "Air Temp (C)", history_temp, 40, -10)

        time.sleep(2.0)

except KeyboardInterrupt:
    device.clear()
    dht_sensor.exit()
    spi.close()
