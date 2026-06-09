import time
import os
import glob
import board
import adafruit_dht
import smbus2
import spidev
from datetime import datetime
from bmp280 import BMP280

# ==========================================
# 1. HARDWARE INITIALIZATION & ERROR HANDLING
# ==========================================

# SPI Bus (MCP3208 -> MQ Sensors & Soil)
try:
    spi = spidev.SpiDev()
    spi.open(0, 0) # SPI Bus 0, CE0
    spi.max_speed_hz = 1000000
    spi_status = "OK"
except Exception as e:
    spi_status = f"ERROR: {e}"

# DHT22 (Air Temp/Hum on GPIO 23)
try:
    dht_sensor = adafruit_dht.DHT22(board.D23)
    dht_status = "OK"
except Exception as e:
    dht_status = f"ERROR: {e}"

# BMP280 (Pressure/Temp via I2C)
try:
    bus = smbus2.SMBus(1)
    bmp = BMP280(i2c_dev=bus, i2c_addr=0x76)
    bmp_status = "OK"
except Exception as e:
    bmp_status = f"ERROR: {e}"

# DS18B20 (Soil Temp via 1-Wire on GPIO 4)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
try:
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    ds18_status = "OK"
except IndexError:
    device_file = None
    ds18_status = "NOT FOUND"

# ==========================================
# 2. SENSOR READ FUNCTIONS
# ==========================================

def read_mcp3208(channel):
    if spi_status != "OK": return 0
    cmd = [0x06 | (channel >> 2), (channel & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

def read_ds18b20():
    if not device_file: return None
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        if lines[0].strip()[-3:] != 'YES': return None
        temp_string = lines[1].find('t=')
        if temp_string != -1:
            return float(lines[1][temp_string+2:]) / 1000.0
    except Exception:
        return None

# ==========================================
# 3. TERMINAL UI DASHBOARD LOOP
# ==========================================
# Soil calibration values (Change these later based on your dry/wet tests)
SOIL_DRY = 4018
SOIL_WET = 2084

# Variables to hold the last successful DHT reading
last_air_t = "Wait..."
last_air_h = "Wait..."

# Clear screen once before starting
os.system('clear')

try:
    while True:
        # --- A. Read Analog Sensors (SPI Bus) ---
        mq7_raw = read_mcp3208(0)   # CH0: MQ-7 (CO)
        mq135_raw = read_mcp3208(1) # CH1: MQ-135 (AQI)
        soil_raw = read_mcp3208(2)  # CH2: Soil Moisture
        
        # Calculate Shielded Voltage for MQs
        mq7_v = (mq7_raw * 3.3) / 4095
        mq135_v = (mq135_raw * 3.3) / 4095
        
        # Calculate Soil Percentage
        soil_pct = 0
        if SOIL_DRY != SOIL_WET: 
            soil_pct = max(0, min(100, ((SOIL_DRY - soil_raw) / (SOIL_DRY - SOIL_WET)) * 100))

        # --- B. Read Digital Sensors ---
        pressure = bmp.get_pressure() if bmp_status == "OK" else 0.0
        
        soil_temp = read_ds18b20()
        soil_temp_str = f"{soil_temp:.1f} °C" if soil_temp else ds18_status

        if dht_status == "OK":
            try:
                # DHT sensors are notorious for random read failures. We catch them here.
                last_air_t = f"{dht_sensor.temperature:.1f} °C"
                last_air_h = f"{dht_sensor.humidity:.1f} %"
            except RuntimeError:
                pass 

        # --- C. Draw UI ---
        # \033[H moves the cursor to the top left without flickering
        print("\033[H", end="")
        print("=========================================================")
        print(f" HICS HARDWARE DIAGNOSTIC ARRAY       TIME: {datetime.now().strftime('%H:%M:%S')}")
        print("=========================================================")
        
        print("\n[ ANALOG SENSORS (SPI Bus) ]")
        if spi_status == "OK":
            print(f" MQ-7   (CO)   | CH0 | Raw: {mq7_raw:4d} | Shield: {mq7_v:.2f} V")
            print(f" MQ-135 (AQI)  | CH1 | Raw: {mq135_raw:4d} | Shield: {mq135_v:.2f} V")
            print(f" Soil Moisture | CH2 | Raw: {soil_raw:4d} | Est: {soil_pct:5.1f} %")
        else:
            print(f" SPI ERROR: {spi_status}")
        
        print("\n[ DIGITAL SENSORS (I2C / 1-Wire / GPIO) ]")
        print(f" DHT22   Air Temp  | GPIO 23 | {last_air_t}")
        print(f" DHT22   Humidity  | GPIO 23 | {last_air_h}")
        print(f" DS18B20 Soil Temp | GPIO  4 | {soil_temp_str}")
        
        if bmp_status == "OK":
            print(f" BMP280  Pressure  | I2C (1) | {pressure:.1f} hPa")
        else:
            print(f" BMP280  Pressure  | I2C (1) | {bmp_status}")

        print("\n=========================================================")
        print("STATUS: ALL SYSTEMS POLLING. Press Ctrl+C to exit.")
        print("\033[J", end="") # Clears any leftover lines below
        
        # 2 seconds is the minimum safe wait time for a DHT22
        time.sleep(2.0)

except KeyboardInterrupt:
    print("\n\nShutting down hardware safely...")
    if spi_status == "OK": spi.close()
    if dht_status == "OK": dht_sensor.exit()
