# Single source of truth for all hardware config.
# Change values here; everything else imports from this file.

# ── GPIO Pins ──────────────────────────────────────────────
DHT22_PIN        = 23   # GPIO 23
DS18B20_BASE_DIR = '/sys/bus/w1/devices/'

# ── I2C Addresses ──────────────────────────────────────────
I2C_BUS     = 1
BMP280_ADDR = 0x76
OLED_ADDR   = 0x3C
RTC_ADDR    = 0x68   # DS3231

# ── SPI / MCP3208 Channels ─────────────────────────────────
# Verify these match your physical perfboard wiring with test_mq.py + test_soil.py
SPI_BUS         = 0
SPI_DEVICE      = 0   # CE0
SPI_SPEED_HZ    = 1_000_000
CH_MQ7          = 0   # MQ-7  CO sensor
CH_MQ135        = 1   # MQ-135 AQI sensor
CH_SOIL         = 2   # Capacitive soil moisture

# ── OLED ───────────────────────────────────────────────────
OLED_WIDTH  = 128
OLED_HEIGHT = 64

# ── Soil Moisture Calibration ──────────────────────────────
# Run scripts/calibrate_soil.py to update these values.
SOIL_DRY = 4018   # raw ADC reading in dry air
SOIL_WET = 2084   # raw ADC reading fully submerged

# ── Database ───────────────────────────────────────────────
DB_PATH = '/home/pawan/iesh_data.db'

# ── Remote API ─────────────────────────────────────────────
API_URL     = 'https://himalayansciences.org/data/api/'
API_KEY     = ''   # set this once you have a key from the site
API_NODE_ID = 'iesh-node-01'

# ── Timing ─────────────────────────────────────────────────
OLED_CYCLE_SECS  = 4    # seconds between OLED screen switches
DB_LOG_SECS      = 60   # seconds between SQLite writes
UPLOAD_SECS      = 300  # seconds between API uploads (5 min)
