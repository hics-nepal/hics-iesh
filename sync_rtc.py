import smbus2
from datetime import datetime

bus = smbus2.SMBus(1)
RTC_ADDRESS = 0x68

def dec_to_bcd(dec):
    """Converts standard decimal to Binary Coded Decimal for the RTC"""
    return (dec // 10 * 16) + (dec % 10)

# Grab the actual time from the Raspberry Pi
now = datetime.now()

try:
    # Write the exact seconds, minutes, hours, day, date, month, and year to the chip
    bus.write_i2c_block_data(RTC_ADDRESS, 0x00, [
        dec_to_bcd(now.second),
        dec_to_bcd(now.minute),
        dec_to_bcd(now.hour),
        dec_to_bcd(now.isoweekday()),
        dec_to_bcd(now.day),
        dec_to_bcd(now.month),
        dec_to_bcd(now.year - 2000)
    ])
    print(f"Success! RTC hardware permanently synced to: {now.strftime('%Y-%m-%d %H:%M:%S')}")
except Exception as e:
    print("Failed to sync RTC. Check wiring.")
    print(e)
