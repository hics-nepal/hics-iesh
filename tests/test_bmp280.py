from bmp280 import BMP280
from smbus2 import SMBus

bus = SMBus(1)
bmp = BMP280(i2c_dev=bus)

print("BMP280 Active")
print(f"Temperature: {bmp.get_temperature():.1f}C")
print(f"Pressure: {bmp.get_pressure():.1f} hPa")
