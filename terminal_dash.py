"""HICS Terminal Dashboard — live sensor readout in the terminal."""
import time
import os
from datetime import datetime

from sensors.dht22 import DHT22
from sensors.bmp280_sensor import BMP280Sensor
from sensors.ds18b20 import DS18B20
from sensors.mcp3208 import MCP3208
from sensors.config import CH_MQ7, CH_MQ135, SOIL_DRY, SOIL_WET

dht   = DHT22()
bmp   = BMP280Sensor()
ds18  = DS18B20()
adc   = MCP3208()

last_air_t = "Wait..."
last_air_h = "Wait..."

os.system('clear')

try:
    while True:
        mq7_raw   = adc.read_raw(CH_MQ7)
        mq135_raw = adc.read_raw(CH_MQ135)
        mq7_v     = adc.read_voltage(CH_MQ7)
        mq135_v   = adc.read_voltage(CH_MQ135)
        soil_pct  = adc.read_soil_pct()
        soil_raw  = adc.read_raw(2)  # raw for display

        _, pressure = bmp.read()
        soil_temp   = ds18.read()
        soil_temp_s = f"{soil_temp:.1f} C" if soil_temp is not None else ds18.error or "N/A"

        t, h = dht.read()
        if t is not None:
            last_air_t = f"{t:.1f} C"
            last_air_h = f"{h:.1f} %"

        print("\033[H", end="")
        print("=" * 57)
        print(f" HICS DIAGNOSTIC              {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 57)

        print("\n[ SPI Analog (MCP3208) ]")
        if adc.ok:
            print(f"  MQ-7  CO    CH{CH_MQ7}  Raw: {mq7_raw:4d}  Voltage: {mq7_v:.3f} V")
            print(f"  MQ-135 AQI  CH{CH_MQ135}  Raw: {mq135_raw:4d}  Voltage: {mq135_v:.3f} V")
            print(f"  Soil Moist  CH2  Raw: {soil_raw:4d}  Est: {soil_pct:5.1f} %")
        else:
            print(f"  SPI ERROR: {adc.error}")

        print("\n[ Digital / I2C / 1-Wire ]")
        print(f"  DHT22  Air Temp   GPIO 23  {last_air_t}")
        print(f"  DHT22  Humidity   GPIO 23  {last_air_h}")
        print(f"  DS18B20 Soil Temp GPIO  4  {soil_temp_s}")
        if bmp.ok:
            print(f"  BMP280 Pressure   I2C 0x76 {pressure:.1f} hPa")
        else:
            print(f"  BMP280 ERROR: {bmp.error}")

        print("\n" + "=" * 57)
        print("Press Ctrl+C to exit.")
        print("\033[J", end="")

        time.sleep(2.0)

except KeyboardInterrupt:
    print("\n\nShutting down...")
    dht.cleanup()
    adc.cleanup()
