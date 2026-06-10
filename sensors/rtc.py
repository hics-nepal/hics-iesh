import smbus2
from datetime import datetime
from .config import I2C_BUS, RTC_ADDR

def _bcd_to_dec(bcd):
    return (bcd >> 4) * 10 + (bcd & 0x0F)

def _dec_to_bcd(dec):
    return (dec // 10 * 16) + (dec % 10)

class RTC:
    def __init__(self):
        self.ok = False
        self.error = None
        try:
            # Just verify the bus opens and device is present — don't read
            bus = smbus2.SMBus(I2C_BUS)
            bus.write_quick(RTC_ADDR)
            bus.close()
            self.ok = True
        except Exception as e:
            self.error = str(e)

    def read(self, retries=5):
        """Returns datetime from DS3231, or None on failure.
        Opens a fresh bus per attempt to avoid stale fd state."""
        if not self.ok:
            return None
        import time
        for attempt in range(retries):
            bus = None
            try:
                bus = smbus2.SMBus(I2C_BUS)
                data   = bus.read_i2c_block_data(RTC_ADDR, 0x00, 7)
                sec    = _bcd_to_dec(data[0] & 0x7F)
                minute = _bcd_to_dec(data[1])
                hour   = _bcd_to_dec(data[2] & 0x3F)
                day    = _bcd_to_dec(data[4])
                month  = _bcd_to_dec(data[5] & 0x1F)
                year   = _bcd_to_dec(data[6]) + 2000
                return datetime(year, month, day, hour, minute, sec)
            except Exception as e:
                self.error = str(e)
                if attempt < retries - 1:
                    time.sleep(0.05)
            finally:
                if bus:
                    bus.close()
        return None

    def sync_from_system(self):
        """Write current system time to DS3231."""
        if not self.ok:
            return False
        now = datetime.now()
        try:
            bus = smbus2.SMBus(I2C_BUS)
            bus.write_i2c_block_data(RTC_ADDR, 0x00, [
                _dec_to_bcd(now.second),
                _dec_to_bcd(now.minute),
                _dec_to_bcd(now.hour),
                _dec_to_bcd(now.isoweekday()),
                _dec_to_bcd(now.day),
                _dec_to_bcd(now.month),
                _dec_to_bcd(now.year - 2000),
            ])
            bus.close()
            return True
        except Exception as e:
            self.error = str(e)
            return False
