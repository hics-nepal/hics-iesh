import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

DRY_VAL = 4018
WET_VAL = 2084

def read_ch(ch):
    cmd = [0x06 | (ch >> 2), (ch & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

print("=== Agri Module: Live Moisture Sensor ===\nPress Ctrl+C to stop.")

try:
    while True:
        raw_val = read_ch(0)
        percentage = max(0, min(100, ((DRY_VAL - raw_val) / (DRY_VAL - WET_VAL)) * 100))
        print(f"Raw: {raw_val:04d}  |  Moisture: {percentage:.1f}%")
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
    print("\nSoil test stopped.")
