import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def read_ch(ch):
    cmd = [0x06 | (ch >> 2), (ch & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

print("=== Agri Module: Soil Calibration ===")

input("1. Hold the sensor in the DRY AIR and press Enter...")
dry_val = read_ch(0)
print(f"--> Dry Baseline Value: {dry_val}\n")

input("2. Dip the sensor into a glass of WATER and press Enter...")
wet_val = read_ch(0)
print(f"--> Wet Baseline Value: {wet_val}\n")

print("Write these two numbers down! You will need them for the final dashboard.")
spi.close()
