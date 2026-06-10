# HICS IESH v0.1

**Himalayan Institute for Contextual Sciences — Integrated Environmental Smart Hub**

An offline-capable environmental monitoring station built on Raspberry Pi. Collects live atmospheric, air quality, and soil data; streams it to a web dashboard; and delivers Nepal CDC-aligned science activities for Grades 6–Undergraduate.

---

## Hardware

| Component | Sensor / Module | Interface |
|-----------|----------------|-----------|
| Air temp & humidity | DHT22 | GPIO 23 |
| Barometric pressure | BMP280 | I2C 0x76 |
| OLED display | SH1106 128×64 | I2C 0x3C |
| Real-time clock | DS3231 | I2C 0x68 |
| Soil temperature | DS18B20 | 1-Wire GPIO 4 |
| Soil moisture | Capacitive (MCP3208 CH2) | SPI |
| CO gas | MQ-7 (MCP3208 CH0) | SPI |
| Air quality | MQ-135 (MCP3208 CH1) | SPI |
| Sky camera | RPi Camera v1.3 OV5647 + fisheye | CSI |
| ADC | MCP3208 8-ch | SPI CE0 |

---

## Quick Start

**Flash a new SD card and have the RPi fully running in one command:**

```bash
# Insert SD card, then:
sudo bash flash.sh --wifi-ssid "YourNetwork" --wifi-password "YourPassword"
```

Then insert the card into the RPi, connect power, and wait 5–10 minutes. Done.

---

## Flashing an SD Card

### What `flash.sh` does

1. Flashes Raspberry Pi OS to the SD card
2. Enables SSH and creates the `pawan` user
3. Configures WiFi
4. Copies all HICS code to the card
5. Installs a first-boot service that automatically installs all dependencies and starts the HICS services on first power-on

The OS image expands to fill the entire SD card on first boot — a 128 GB card will use all 128 GB.

### Requirements

- Linux machine with the SD card inserted
- `sudo` access
- Tools: `dd`, `xzcat` (`xz-utils`), `rsync`, `partprobe` (`parted`)
- Raspberry Pi OS image (`.img` or `.img.xz`) — download from [raspberrypi.com/software/operating-systems](https://www.raspberrypi.com/software/operating-systems/) or use the one in `~/Downloads`

### Usage

```bash
# Basic (will prompt for WiFi)
sudo bash flash.sh

# Full options
sudo bash flash.sh \
  --image ~/Downloads/2026-04-21-raspios-trixie-arm64-lite.img.xz \
  --device /dev/sda \
  --wifi-ssid "MyNetwork" \
  --wifi-password "MyPassword" \
  --hostname "hics-iesh" \
  --password "***"

# Only flash OS without copying HICS code
sudo bash flash.sh --skip-code
```

| Option | Default | Description |
|--------|---------|-------------|
| `--image PATH` | auto-detect `~/Downloads/*.img.xz` | OS image file |
| `--device DEV` | `/dev/sda` | SD card device (confirmed before writing) |
| `--wifi-ssid` | (prompted) | WiFi network name |
| `--wifi-password` | (prompted) | WiFi password |
| `--hostname` | `hics-iesh` | RPi hostname |
| `--password` | `***` | `pawan` user password |
| `--skip-code` | false | Skip copying HICS code |

### After First Boot

First boot takes **5–10 minutes** while packages install. When complete:

```bash
# Find the RPi on your network
ping hics-iesh.local

# SSH in
ssh pawan@hics-iesh.local   # password: ***

# Check first-boot completed
cat ~/hics-firstboot.log

# Check services
sudo systemctl status hics-core hics-web
```

Open the dashboard in any browser: **`http://hics-iesh.local:5000/`**

---

## Manual Setup (no flash.sh)

If you already have RPi OS running and just want to install HICS:

```bash
# On RPi — copy code first, then:
sudo bash ~/hics/setup.sh
```

`setup.sh` installs packages, enables hardware interfaces, configures the DB path, installs systemd services, and runs sensor tests. Safe to re-run.

---

## Accessing the Station

| URL | Description |
|-----|-------------|
| `http://<ip>:5000/` | Main dashboard — live sensor data |
| `http://<ip>:5000/camera` | Sky camera — live stream + still |
| `http://<ip>:5000/learn` | Learning portal — 5 modules, 25+ activities |

Default SSH: `ssh pawan@<ip>` or `ssh pawan@hics-iesh.local` — password: `***`

---

## SD Card Migration (moving to a bigger card)

```bash
# 1. Flash new card (same command as above)
sudo bash flash.sh --wifi-ssid "..." --wifi-password "..."

# 2. Optionally copy existing database to new card
#    (connect old RPi via SSH first, or mount old card)
scp pawan@<old-ip>:~/hics-data/hics.db /tmp/hics.db
# Then after flashing and booting:
scp /tmp/hics.db pawan@<new-ip>:~/hics-data/hics.db
```

The data directory (`~/hics-data/`) is separate from the code so the database survives code updates and re-flashes.

---

## Creating a Reusable Custom Image

After the RPi is fully set up, you can create a custom `.img.xz` to flash to other cards instantly (no first-boot wait):

```bash
# On development machine, with RPi card inserted as /dev/sda:
# (RPi must be powered off and card removed)

# Shrink partitions first (optional but recommended)
sudo apt install pishrink
sudo pishrink.sh /tmp/hics-custom.img   # if you dd'd first

# Or just dd the card directly:
sudo dd if=/dev/sda bs=4M status=progress | xz -T0 > hics-custom.img.xz
```

This image can be flashed to any card with `flash.sh --image hics-custom.img.xz --skip-code` (code is already embedded) or standard tools.

---

## Development Workflow

Changes made on your development machine are synced to the running RPi:

```bash
# Sync code changes
./deploy.sh

# Sync + restart Flask
./deploy.sh   # then manually restart:
ssh pawan@<rpi-ip> "kill \$(pgrep -f web/app.py); cd ~/hics && nohup python3 web/app.py >> /tmp/web.log 2>&1 &"
```

The `deploy.sh` script uses `rsync --relative` — never use bare `rsync` with multiple sources as it silently flattens paths.

### Service management on RPi

```bash
sudo systemctl status hics-core hics-web      # check status
sudo systemctl restart hics-web               # restart web server
journalctl -u hics-web -f                     # live web logs
journalctl -u hics-core -f                    # live sensor logs
```

### Run sensor tests

```bash
ssh pawan@<rpi-ip> "sudo python3 ~/hics/tests/test_all.py"
```

---

## Project Structure

```
hics-iesh-v0.1/
├── flash.sh                   ← Flash SD card (run on dev machine)
├── setup.sh                   ← Install/repair on running RPi (run on RPi)
├── deploy.sh                  ← Sync code from dev machine to RPi
├── requirements.txt           ← Python dependencies
│
├── core_dash.py               ← OLED display + sensor loop + DB logger
├── terminal_dash.py           ← Terminal monitoring dashboard
│
├── sensors/
│   ├── config.py              ← All hardware config (single source of truth)
│   ├── camera.py              ← Sky camera: capture, analysis, MJPEG stream
│   ├── bmp280_sensor.py       ← Pressure / temperature
│   ├── dht22.py               ← Air temp / humidity
│   ├── ds18b20.py             ← Soil temperature
│   ├── mcp3208.py             ← ADC: soil moisture + MQ gas sensors
│   ├── oled.py                ← SH1106 OLED display
│   └── rtc.py                 ← DS3231 real-time clock
│
├── data/
│   ├── database.py            ← SQLite read/write interface
│   └── uploader.py            ← Remote API uploader
│
├── web/
│   ├── app.py                 ← Flask app (port 5000)
│   ├── static/style.css       ← Shared styles
│   └── templates/
│       ├── index.html         ← Main dashboard
│       ├── camera.html        ← Sky camera page
│       ├── _nav.html          ← Shared navigation
│       └── learn/             ← Learning portal templates
│
├── curriculum/
│   └── modules/               ← 5 learning modules (climate, soil, air, data, environment)
│
├── scripts/
│   ├── firstboot.sh           ← Runs on RPi at first power-on (auto-setup)
│   ├── calibrate_soil.py      ← Soil moisture calibration
│   └── sync_rtc.py            ← RTC time sync utility
│
├── services/
│   ├── hics-core.service      ← Systemd: sensor loop
│   ├── hics-web.service       ← Systemd: Flask web server
│   └── hics-firstboot.service ← Systemd: runs firstboot.sh once
│
└── tests/
    ├── test_all.py            ← Master test runner
    ├── test_camera.py         ← Camera capture + sky analysis
    └── test_*.py              ← Per-sensor tests
```

---

## Troubleshooting

### Web app won't start
```bash
journalctl -u hics-web -n 50 --no-pager
sudo lsof -i :5000       # check for port conflict
```

### Sensors reading None
```bash
sudo python3 ~/hics/tests/test_all.py   # run all sensor tests
i2cdetect -y 1                           # I2C bus scan
# Expected: 0x3C (OLED), 0x68 (RTC), 0x76 (BMP280)
ls /sys/bus/w1/devices/                  # 1-Wire (DS18B20)
```

### Camera not working
```bash
rpicam-hello --list-cameras             # should show OV5647
rpicam-still -o /tmp/test.jpg && ls -lh /tmp/test.jpg
# If not detected: check ribbon cable, then rerun: sudo bash ~/hics/setup.sh
```

### No data in charts (blank dashboard)
```bash
journalctl -u hics-core -n 30 --no-pager
sqlite3 ~/hics-data/hics.db "SELECT COUNT(*), MAX(timestamp) FROM telemetry;"
```

### First boot seems stuck
```bash
# SSH in and check the log
ssh pawan@hics-iesh.local
cat ~/hics-firstboot.log
sudo systemctl status hics-firstboot
```

### SD card / disk space
```bash
df -h
sqlite3 ~/hics-data/hics.db \
  "DELETE FROM telemetry WHERE timestamp < datetime('now','-30 days'); VACUUM;"
```

### WiFi (wlan1 internet adapter)
```bash
sudo nmcli dev wifi connect 'SSID' password 'PASSWORD' ifname wlan1
```

---

## Learning Portal

**`http://<ip>:5000/learn`**

5 modules, 25+ activities for Grades 6–Undergraduate aligned with Nepal CDC:

| Module | Focus | Grade range |
|--------|-------|-------------|
| 🌡️ Climate | Temperature, humidity, pressure, altitude | 6–UG |
| 🌱 Soil | Moisture, temperature, agriculture | 6–UG |
| 💨 Air Quality | CO, gas sensors, AQI | 6–UG |
| 📊 Data Science | Statistics, sensor patterns | 6–UG |
| 🌍 Environment | Ecology, policy, altitude zones | 6–UG |

Grade 6–8 activities include live sensor visualizations (horizontal gauges, bar charts, sky camera, altitude zones) that update in real time from the station.

---

*Built by [HICS — Himalayan Institute for Contextual Sciences](https://himalayansciences.org)*
