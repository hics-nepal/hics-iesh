import spidev
from .config import SPI_BUS, SPI_DEVICE, SPI_SPEED_HZ, CH_SOIL, SOIL_DRY, SOIL_WET

class MCP3208:
    def __init__(self):
        self.ok = False
        self.error = None
        try:
            self._spi = spidev.SpiDev()
            self._spi.open(SPI_BUS, SPI_DEVICE)
            self._spi.max_speed_hz = SPI_SPEED_HZ
            self.ok = True
        except Exception as e:
            self.error = str(e)

    def read_raw(self, channel):
        """Raw 12-bit ADC value (0–4095) for the given channel."""
        if not self.ok:
            return 0
        cmd = [0x06 | (channel >> 2), (channel & 0x03) << 6, 0x00]
        r = self._spi.xfer2(cmd)
        return ((r[1] & 0x0F) << 8) | r[2]

    def read_voltage(self, channel, vref=3.3):
        """Voltage at the given channel."""
        return (self.read_raw(channel) * vref) / 4095

    def read_soil_pct(self):
        """Soil moisture as 0–100%. Calibrate SOIL_DRY/SOIL_WET in config.py."""
        raw = self.read_raw(CH_SOIL)
        if SOIL_DRY == SOIL_WET:
            return 0.0
        return max(0.0, min(100.0, ((SOIL_DRY - raw) / (SOIL_DRY - SOIL_WET)) * 100))

    def cleanup(self):
        if self.ok:
            try:
                self._spi.close()
            except Exception:
                pass
