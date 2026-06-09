import smbus2
from bmp280 import BMP280
from .config import I2C_BUS, BMP280_ADDR

class BMP280Sensor:
    def __init__(self):
        self.ok = False
        self.error = None
        try:
            bus = smbus2.SMBus(I2C_BUS)
            self._sensor = BMP280(i2c_dev=bus, i2c_addr=BMP280_ADDR)
            self.ok = True
        except Exception as e:
            self.error = str(e)

    def read(self):
        """Returns (temperature_C, pressure_hPa) or (None, None) on failure."""
        if not self.ok:
            return None, None
        try:
            return self._sensor.get_temperature(), self._sensor.get_pressure()
        except Exception as e:
            self.error = str(e)
            return None, None
