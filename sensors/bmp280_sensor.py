import struct
import smbus2
from .config import I2C_BUS, BMP280_ADDR


class BMP280Sensor:
    """Direct BMP280 driver via smbus2.

    The pimoroni `bmp280` library left the chip in sleep mode with
    measurements skipped (ctrl_meas=0x00), so the data registers never
    refreshed and every read returned the same stale pressure forever.
    This driver puts the chip in continuous (normal) mode at init and
    compensates readings per the Bosch datasheet (float variant).
    """

    REG_ID        = 0xD0
    REG_CTRL_MEAS = 0xF4
    REG_CONFIG    = 0xF5
    REG_DATA      = 0xF7
    REG_CALIB     = 0x88
    CHIP_ID       = 0x58

    def __init__(self):
        self.ok = False
        self.error = None
        try:
            self._bus = smbus2.SMBus(I2C_BUS)
            self._addr = BMP280_ADDR
            cid = self._bus.read_byte_data(self._addr, self.REG_ID)
            if cid != self.CHIP_ID:
                raise RuntimeError(f"chip id 0x{cid:02X}, expected 0x58")
            self._read_calibration()
            # config: standby 500 ms, IIR filter x4 (smooths pressure noise)
            self._bus.write_byte_data(self._addr, self.REG_CONFIG, 0x88)
            # ctrl_meas: osrs_t=x2, osrs_p=x16, mode=normal (continuous)
            self._bus.write_byte_data(self._addr, self.REG_CTRL_MEAS, 0x57)
            self.ok = True
        except Exception as e:
            self.error = str(e)

    def _read_calibration(self):
        raw = bytes(self._bus.read_i2c_block_data(self._addr, self.REG_CALIB, 24))
        # T1,P1 unsigned; the rest signed; all little-endian 16-bit
        (self._T1, self._T2, self._T3,
         self._P1, self._P2, self._P3, self._P4, self._P5,
         self._P6, self._P7, self._P8, self._P9) = struct.unpack(
            '<HhhHhhhhhhhh', raw)

    def read(self):
        """Returns (temperature_C, pressure_hPa) or (None, None) on failure."""
        if not self.ok:
            return None, None
        try:
            d = self._bus.read_i2c_block_data(self._addr, self.REG_DATA, 6)
            raw_p = (d[0] << 12) | (d[1] << 4) | (d[2] >> 4)
            raw_t = (d[3] << 12) | (d[4] << 4) | (d[5] >> 4)
            if raw_t in (0, 0x80000, 0xFFFFF):
                # Skip value = chip reset to sleep mode (undervoltage brownout
                # does this). Re-arm continuous mode; next read will be live.
                self._bus.write_byte_data(self._addr, self.REG_CONFIG, 0x88)
                self._bus.write_byte_data(self._addr, self.REG_CTRL_MEAS, 0x57)
                return None, None

            # Bosch datasheet float compensation
            var1 = (raw_t / 16384.0 - self._T1 / 1024.0) * self._T2
            var2 = ((raw_t / 131072.0 - self._T1 / 8192.0) ** 2) * self._T3
            t_fine = var1 + var2
            temp = t_fine / 5120.0

            var1 = t_fine / 2.0 - 64000.0
            var2 = var1 * var1 * self._P6 / 32768.0
            var2 = var2 + var1 * self._P5 * 2.0
            var2 = var2 / 4.0 + self._P4 * 65536.0
            var1 = (self._P3 * var1 * var1 / 524288.0
                    + self._P2 * var1) / 524288.0
            var1 = (1.0 + var1 / 32768.0) * self._P1
            if var1 == 0:
                return temp, None
            p = 1048576.0 - raw_p
            p = (p - var2 / 4096.0) * 6250.0 / var1
            var1 = self._P9 * p * p / 2147483648.0
            var2 = p * self._P8 / 32768.0
            p = p + (var1 + var2 + self._P7) / 16.0
            return temp, p / 100.0
        except Exception as e:
            self.error = str(e)
            return None, None
