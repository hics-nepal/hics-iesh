import spidev
from .config import (
    SPI_BUS, SPI_DEVICE, SPI_SPEED_HZ,
    CH_SOIL, SOIL_DRY, SOIL_WET,
    MQ_DIVIDER_RATIO, MQ_VCC, MQ_RL_OHM,
)

_VREF = 3.3   # MCP3208 reference voltage


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

    def read_voltage(self, channel):
        """Voltage at the ADC input pin (0–3.3V, i.e. post-divider for MQ channels)."""
        return (self.read_raw(channel) * _VREF) / 4095

    def read_sensor_voltage(self, channel):
        """True voltage at the MQ sensor AOUT pin, corrected for the 2× voltage divider.
        Use this for RS/R0 calculations. Returns 0.0–5.0V."""
        return self.read_voltage(channel) * MQ_DIVIDER_RATIO

    def read_mq_rs(self, channel):
        """Sensor resistance RS in Ohms. Returns None if sensor voltage is ~0.
        RS = RL * (VCC / VOUT_sensor - 1).
        Useful for RS/R0 ratio once R0 is measured in clean air."""
        v = self.read_sensor_voltage(channel)
        if v < 0.01:
            return None
        return MQ_RL_OHM * (MQ_VCC / v - 1.0)

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
