import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def read_mcp3208(channel):
    cmd = [0x06 | (channel >> 2), (channel & 0x03) << 6, 0x00]
    r = spi.xfer2(cmd)
    return ((r[1] & 0x0F) << 8) | r[2]

print("Testing MCP3208 SPI Connection... Press Ctrl+C to stop.")

try:
    while True:
        print(f"CH0: {read_mcp3208(0):04d}  CH1: {read_mcp3208(1):04d}  CH2: {read_mcp3208(2):04d}")
        time.sleep(0.5)
except KeyboardInterrupt:
    spi.close()
    print("\nSPI Test Stopped.")
