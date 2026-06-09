import os
import glob
from .config import DS18B20_BASE_DIR

class DS18B20:
    def __init__(self):
        self.ok = False
        self.error = None
        self._device_file = None
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        try:
            folders = glob.glob(DS18B20_BASE_DIR + '28*')
            if not folders:
                self.error = 'No DS18B20 found on 1-Wire bus'
                return
            self._device_file = folders[0] + '/w1_slave'
            self.ok = True
        except Exception as e:
            self.error = str(e)

    def read(self):
        """Returns temperature in °C or None on failure."""
        if not self.ok:
            return None
        try:
            with open(self._device_file, 'r') as f:
                lines = f.readlines()
            if lines[0].strip()[-3:] != 'YES':
                return None
            pos = lines[1].find('t=')
            if pos != -1:
                return float(lines[1][pos + 2:]) / 1000.0
        except Exception:
            return None
