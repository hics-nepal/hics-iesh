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

    def read(self, retries=5, delay=2.5):
        """Returns (temperature_C, humidity_pct) or (None, None) after retries.
        DHT22 bit-banging on kernel 6.x has ~50% success rate per attempt."""
        if not self.ok:
            return None, None
        import time
        for _ in range(retries):
            try:
                t = self._sensor.temperature
                h = self._sensor.humidity
                if t is not None and h is not None:
                    return t, h
            except RuntimeError:
                pass
            time.sleep(delay)
        return None, None

    def cleanup(self):
        if self.ok:
            try:
                self._sensor.exit()
            except Exception:
                pass
