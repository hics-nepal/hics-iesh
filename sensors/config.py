# Single source of truth for all hardware config.
# Change values here; everything else imports from this file.

# GPIO Pins
DHT22_PIN        = 23   # GPIO 23
DS18B20_BASE_DIR = '/sys/bus/w1/devices/'

# I2C Addresses
I2C_BUS     = 1
BMP280_ADDR = 0x76
OLED_ADDR   = 0x3C
RTC_ADDR    = 0x68   # DS3231

# SPI / MCP3208 Channels
SPI_BUS         = 0
SPI_DEVICE      = 0   # CE0
SPI_SPEED_HZ    = 1_000_000
CH_MQ7          = 0   # MQ-7  CO sensor
CH_MQ135        = 1   # MQ-135 AQI sensor
CH_SOIL         = 2   # Capacitive soil moisture

# MQ Sensor Voltage Divider
# Two 4.7kΩ resistors halve the MQ AOUT (0–5V) to 0–2.5V safe for VREF=3.3V.
# MQ_DIVIDER_RATIO corrects ADC voltage back to the true sensor output voltage.
# MQ_VCC is the sensor supply (heater + AOUT reference).
MQ_DIVIDER_RATIO = 2.0   # (R1+R2)/R2 = (4.7+4.7)/4.7
MQ_VCC           = 5.0   # V — sensor supply rail
# MQ_RL: load resistor on the MQ module board (1kΩ on most blue modules).
# Used to compute RS = MQ_RL * (MQ_VCC / sensor_voltage - 1).
# Check your module datasheet or measure with multimeter between AOUT and GND
# with sensor disconnected. Leave as None if unknown — RS won't be computed.
MQ_RL_OHM        = 1000  # Ω — adjust if your module differs

# OLED
OLED_WIDTH  = 128
OLED_HEIGHT = 64

# Soil Moisture Calibration
# Run scripts/calibrate_soil.py to update these values.
SOIL_DRY = 4018   # raw ADC reading in dry air
SOIL_WET = 2084   # raw ADC reading fully submerged

# Location & Altitude
NODE_LOCATION = 'HICS Station, Nepal'
SEA_LEVEL_HPA = 1013.25   # reference sea-level pressure for altitude calc

# Database
DB_PATH = '/home/pawan/hics-data/hics.db'

# Remote API
API_URL     = 'https://himalayansciences.org/data/api/'
API_KEY     = ''   # set this once you have a key from the site
API_NODE_ID = 'iesh-node-01'

# Network
HOTSPOT_SSID   = 'IESH_Hub'
HOTSPOT_IP     = '10.42.0.1'
HOTSPOT_IFACE  = 'wlan0'
INTERNET_IFACE = 'wlan1'

# Timing
OLED_CYCLE_SECS = 5    # seconds between OLED screen switches
DB_LOG_SECS     = 60   # seconds between SQLite writes
UPLOAD_SECS     = 300  # seconds between API uploads (5 min)
