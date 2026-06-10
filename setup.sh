#!/usr/bin/env bash
# =============================================================================
# HICS IESH — Full System Setup for Raspberry Pi
# =============================================================================
# Usage:  sudo bash setup.sh
#
# Idempotent — safe to re-run after partial failure or upgrades.
# Tested on Raspberry Pi OS Bookworm (Debian 12) with RPi Zero 2W / 3B / 4.
#
# SD card migration: flash fresh Raspberry Pi OS Lite, enable SSH, copy or
# clone this repo to ~/hics, then run: sudo bash ~/hics/setup.sh
# =============================================================================

set -euo pipefail

# ── Colour helpers ────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
info()  { echo -e "${CYAN}[→]${NC} $*"; }
ok()    { echo -e "${GREEN}[✓]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
fail()  { echo -e "${RED}[✗]${NC} $*"; exit 1; }
section(){ echo; echo -e "${BOLD}${CYAN}━━━ $* ━━━${NC}"; echo; }

# ── Must run as root ──────────────────────────────────────────────────────────
[[ $EUID -eq 0 ]] || fail "Run with sudo: sudo bash setup.sh"

# ── Locate repo and app user ──────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_USER="${SUDO_USER:-pawan}"
APP_HOME="/home/${APP_USER}"
HICS_DIR="${APP_HOME}/hics"
DATA_DIR="${APP_HOME}/hics-data"

echo
echo -e "${BOLD}╔══════════════════════════════════════╗"
echo -e "║    HICS IESH — System Setup          ║"
echo -e "╚══════════════════════════════════════╝${NC}"
info "Repo :   $SCRIPT_DIR"
info "App dir: $HICS_DIR"
info "Data dir:$DATA_DIR"
info "User:    $APP_USER"

# ── 1. System prerequisites ───────────────────────────────────────────────────
section "1 / 7  System packages"

info "Running apt-get update..."
apt-get update -qq

PKGS=(
  python3-pip python3-dev git sqlite3
  i2c-tools python3-smbus
  python3-pil                    # Pillow (system package — faster than pip)
  libcamera-apps rpicam-apps     # rpicam-still, rpicam-vid
  python3-libcamera              # Python libcamera bindings (optional)
  ntpdate                        # time sync on boot
  vim curl wget                  # utilities
)

# Install only what's missing
MISSING=()
for pkg in "${PKGS[@]}"; do
  dpkg -s "$pkg" &>/dev/null || MISSING+=("$pkg")
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
  info "Installing: ${MISSING[*]}"
  apt-get install -y -q "${MISSING[@]}" || warn "Some packages failed — continuing"
else
  ok "All system packages already installed"
fi

# ── 2. Python packages via pip ────────────────────────────────────────────────
section "2 / 7  Python packages (pip)"

PIP_FLAGS="--break-system-packages --quiet"
REQ_FILE="${SCRIPT_DIR}/requirements.txt"

if [[ -f "$REQ_FILE" ]]; then
  info "Installing from requirements.txt..."
  sudo -u "$APP_USER" pip3 install $PIP_FLAGS -r "$REQ_FILE" \
    || warn "Some pip packages failed — check requirements.txt"
  ok "pip install complete"
else
  warn "requirements.txt not found at $REQ_FILE — skipping pip install"
fi

# ── 3. Hardware interfaces ────────────────────────────────────────────────────
section "3 / 7  Hardware interfaces"

enable_iface() {
  local name="$1" key="$2" file="/boot/firmware/config.txt"
  # Bookworm uses /boot/firmware/config.txt; Bullseye uses /boot/config.txt
  [[ -f "$file" ]] || file="/boot/config.txt"
  if grep -q "^dtparam=${key}=on" "$file" 2>/dev/null; then
    ok "$name already enabled"
  else
    echo "dtparam=${key}=on" >> "$file"
    ok "$name enabled (reboot required)"
    NEED_REBOOT=1
  fi
}

enable_overlay() {
  local name="$1" overlay="$2" file="/boot/firmware/config.txt"
  [[ -f "$file" ]] || file="/boot/config.txt"
  if grep -q "^dtoverlay=${overlay}" "$file" 2>/dev/null; then
    ok "$name already enabled"
  else
    echo "dtoverlay=${overlay}" >> "$file"
    ok "$name overlay added (reboot required)"
    NEED_REBOOT=1
  fi
}

NEED_REBOOT=0
enable_iface "I2C"     "i2c_arm"
enable_iface "SPI"     "spi"
enable_iface "1-Wire"  "w1-gpio"
# Camera — libcamera works without legacy camera enable on Bookworm
# But loading the overlay ensures the camera is detected:
enable_overlay "Camera" "ov5647"

# Ensure I2C module loads now (without reboot):
modprobe i2c-dev 2>/dev/null && ok "i2c-dev module loaded" || true
modprobe w1-gpio 2>/dev/null && ok "w1-gpio module loaded" || true

# ── 4. Directories and data ───────────────────────────────────────────────────
section "4 / 7  Directories and data"

# Code directory: should already exist (cloned repo)
if [[ ! -d "$HICS_DIR" ]]; then
  warn "HICS code not found at $HICS_DIR"
  if [[ "$SCRIPT_DIR" != "$HICS_DIR" ]]; then
    info "Copying from $SCRIPT_DIR to $HICS_DIR..."
    mkdir -p "$HICS_DIR"
    rsync -a --exclude='.git' "${SCRIPT_DIR}/" "${HICS_DIR}/"
    chown -R "${APP_USER}:${APP_USER}" "$HICS_DIR"
    ok "Code copied to $HICS_DIR"
  else
    fail "Code directory missing and cannot auto-copy. Clone the repo to ~/hics first."
  fi
else
  ok "Code directory: $HICS_DIR"
fi

# Data directory for SQLite database (outside code dir — survives git pulls)
mkdir -p "$DATA_DIR"
chown "${APP_USER}:${APP_USER}" "$DATA_DIR"
ok "Data directory: $DATA_DIR"

# Update DB_PATH in sensors/config.py if it still points to the old location
CONFIG_FILE="${HICS_DIR}/sensors/config.py"
if grep -q "iesh_data.db" "$CONFIG_FILE" 2>/dev/null; then
  sed -i "s|DB_PATH = '.*'|DB_PATH = '${DATA_DIR}/hics.db'|" "$CONFIG_FILE"
  chown "${APP_USER}:${APP_USER}" "$CONFIG_FILE"
  ok "DB_PATH updated → ${DATA_DIR}/hics.db"
fi

# Migrate existing database if it lives in the old location
OLD_DB="${APP_HOME}/iesh_data.db"
NEW_DB="${DATA_DIR}/hics.db"
if [[ -f "$OLD_DB" && ! -f "$NEW_DB" ]]; then
  cp "$OLD_DB" "$NEW_DB"
  chown "${APP_USER}:${APP_USER}" "$NEW_DB"
  ok "Database migrated: $OLD_DB → $NEW_DB"
elif [[ -f "$NEW_DB" ]]; then
  ok "Database exists: $NEW_DB"
else
  info "No existing database — will be created on first run"
fi

# ── 5. Systemd services ───────────────────────────────────────────────────────
section "5 / 7  Systemd services"

install_service() {
  local src="${HICS_DIR}/services/${1}" dst="/etc/systemd/system/${1}"
  if [[ ! -f "$src" ]]; then
    warn "Service file not found: $src"
    return
  fi
  cp "$src" "$dst"
  ok "Installed $1"
}

install_service "hics-core.service"
install_service "hics-web.service"

systemctl daemon-reload
systemctl enable hics-core hics-web
ok "Services enabled (will start on next boot)"

# Start them now
for svc in hics-core hics-web; do
  if systemctl is-active --quiet "$svc"; then
    info "$svc already running — restarting with new code..."
    systemctl restart "$svc"
    ok "$svc restarted"
  else
    systemctl start "$svc" && ok "$svc started" || warn "$svc failed to start (check: journalctl -u $svc)"
  fi
done

# ── 6. Verification ───────────────────────────────────────────────────────────
section "6 / 7  Verification"

sleep 3   # give services a moment to settle

# Web server responds?
if curl -s --max-time 5 http://localhost:5000/ > /dev/null; then
  ok "Web dashboard: http://localhost:5000/ → OK"
else
  warn "Web dashboard not responding yet — may still be starting up"
fi

# Camera available?
if rpicam-still --list-cameras 2>&1 | grep -q 'Available cameras'; then
  ok "Camera: detected"
else
  warn "Camera: not detected — check ribbon cable and overlay"
fi

# I2C bus scan
if command -v i2cdetect &>/dev/null; then
  info "I2C devices on bus 1:"
  i2cdetect -y 1 2>/dev/null | grep -v "^$" | sed 's/^/    /' || true
fi

# Run sensor tests as the app user
info "Running sensor tests (may take ~30 s)..."
sudo -u "$APP_USER" python3 "${HICS_DIR}/tests/test_all.py" 2>&1 | tail -20 || warn "Some sensor tests failed"

# ── 7. Summary ────────────────────────────────────────────────────────────────
section "7 / 7  Summary"

IP=$(hostname -I | awk '{print $1}')

ok "Setup complete!"
echo
echo -e "  ${BOLD}Dashboard:${NC}   http://${IP}:5000/"
echo -e "  ${BOLD}Camera:${NC}      http://${IP}:5000/camera"
echo -e "  ${BOLD}Learn:${NC}       http://${IP}:5000/learn"
echo -e "  ${BOLD}Data:${NC}        ${DATA_DIR}/hics.db"
echo -e "  ${BOLD}Logs:${NC}        journalctl -u hics-web -f"
echo
if [[ $NEED_REBOOT -eq 1 ]]; then
  echo -e "${YELLOW}  ⚠  Hardware interfaces were changed — REBOOT REQUIRED${NC}"
  echo -e "     Run: sudo reboot"
fi

# ── Troubleshooting guide ─────────────────────────────────────────────────────
cat << 'TROUBLESHOOT'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TROUBLESHOOTING GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Web app won't start
  ─────────────────────────────────────────────────────
  journalctl -u hics-web -n 50 --no-pager
  # Common causes: missing Python package, port 5000 in use
  # Fix port conflict: sudo lsof -i :5000

  Sensor reads None / error
  ─────────────────────────────────────────────────────
  sudo python3 ~/hics/tests/test_all.py     # full test run
  i2cdetect -y 1                             # check I2C addresses
  # BMP280 should appear at 0x76, OLED at 0x3C, RTC at 0x68
  ls /sys/bus/w1/devices/                    # check 1-Wire (DS18B20)
  # If no devices: sudo modprobe w1-gpio

  Camera not working
  ─────────────────────────────────────────────────────
  rpicam-hello --list-cameras               # lists detected cameras
  rpicam-still -o /tmp/test.jpg && ls -lh /tmp/test.jpg
  # If camera not listed: check ribbon cable orientation, run setup.sh again
  # after physically reseating the cable, then reboot

  No data in dashboard (blank charts)
  ─────────────────────────────────────────────────────
  journalctl -u hics-core -n 30 --no-pager
  # Core service logs every 60s; check for sensor errors
  sqlite3 ~/hics-data/hics.db "SELECT COUNT(*), MAX(timestamp) FROM telemetry;"
  # If count is 0: core service has never logged — check above

  WiFi (wlan1) not connecting
  ─────────────────────────────────────────────────────
  sudo nmcli dev wifi connect 'SSID' password 'PASSWORD' ifname wlan1
  nmcli connection show                      # list all connections
  ip addr show wlan1                         # check IP assigned

  SD card full
  ─────────────────────────────────────────────────────
  df -h                                      # check disk usage
  du -sh ~/hics-data/hics.db                # DB size
  # Trim old telemetry (keep last 30 days):
  sqlite3 ~/hics-data/hics.db \
    "DELETE FROM telemetry WHERE timestamp < datetime('now','-30 days');"
  sqlite3 ~/hics-data/hics.db "VACUUM;"

  Restore / SD card migration
  ─────────────────────────────────────────────────────
  1. Flash fresh Raspberry Pi OS Lite on new card
  2. Create /boot/firmware/ssh (enable SSH on first boot)
  3. Configure WiFi via /boot/firmware/wpa_supplicant.conf or raspi-config
  4. SSH in, copy or git-clone repo to ~/hics:
       scp -r /path/to/hics-iesh-v0.1 pawan@<newip>:~/hics
  5. Copy database:
       scp ~/hics-data/hics.db pawan@<newip>:~/hics-data/
  6. Run: sudo bash ~/hics/setup.sh
  7. Done.

  Service status quick check
  ─────────────────────────────────────────────────────
  systemctl status hics-core hics-web       # service health
  journalctl -u hics-web -f                 # live web log
  journalctl -u hics-core -f               # live sensor log
  sudo systemctl restart hics-web           # restart web
  sudo systemctl restart hics-core          # restart sensor loop

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TROUBLESHOOT
