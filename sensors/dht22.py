import board
import adafruit_dht
from .config import DHT22_PIN

_PIN_MAP = {23: board.D23}

class DHT22:
    def __init__(self):
        self.ok = False
        self.error = None
        try:
            pin = _PIN_MAP.get(DHT22_PIN, board.D23)
            self._sensor = adafruit_dht.DHT22(pin, use_pulseio=False)
            self.ok = True
        except Exception as e:
            self.error = str(e)

    def read(self):
        """Returns (temperature_C, humidity_pct) or (None, None) on failure."""
        if not self.ok:
            return None, None
        try:
            return self._sensor.temperature, self._sensor.humidity
        except RuntimeError:
            return None, None

    def cleanup(self):
        if self.ok:
            try:
                self._sensor.exit()
            except Exception:
                pass
