#!/usr/bin/env bash
# =============================================================================
# HICS IESH — First Boot Setup Script
# =============================================================================
# Runs automatically on the Raspberry Pi at first power-on via the
# hics-firstboot.service systemd unit. Installs all dependencies,
# enables hardware interfaces, starts the HICS services, then disables
# itself so it never runs again.
#
# Do NOT run this manually — use setup.sh for manual re-runs.
# =============================================================================

set -uo pipefail   # don't set -e: non-critical failures should be logged, not abort

LOG="/home/pawan/hics-firstboot.log"
HICS_DIR="/home/pawan/hics"
DATA_DIR="/home/pawan/hics-data"
MARKER="${HICS_DIR}/.firstboot-complete"
BOOT_DIR="/boot/firmware"

# ── Guard: only run once ──────────────────────────────────────────────────────
if [[ -f "$MARKER" ]]; then
  echo "[firstboot] Already completed at $(cat "$MARKER") — exiting." | tee -a "$LOG"
  exit 0
fi

# ── Logging setup ─────────────────────────────────────────────────────────────
exec > >(tee -a "$LOG") 2>&1
echo "========================================================"
echo "  HICS First Boot — $(date)"
echo "========================================================"

step() { echo; echo "── $* ──"; }
ok()   { echo "  [OK] $*"; }
warn() { echo "  [!]  $*"; }

# ── Step 1: Apply hostname ────────────────────────────────────────────────────
step "Hostname"
HOSTNAME_FILE="${BOOT_DIR}/hics-hostname.txt"
if [[ -f "$HOSTNAME_FILE" ]]; then
  NEW_HOSTNAME=$(cat "$HOSTNAME_FILE" | tr -d '[:space:]')
  if [[ -n "$NEW_HOSTNAME" ]]; then
    hostnamectl set-hostname "$NEW_HOSTNAME" 2>/dev/null && ok "Hostname set: $NEW_HOSTNAME" || warn "hostnamectl failed"
    sed -i "s/127\.0\.1\.1.*/127.0.1.1\t${NEW_HOSTNAME}/" /etc/hosts 2>/dev/null || true
  fi
fi

# ── Step 2: Wait for network ──────────────────────────────────────────────────
step "Network"
echo "  Waiting for internet connectivity (up to 90s)..."
CONNECTED=false
for i in $(seq 1 18); do
  if ping -c1 -W3 8.8.8.8 &>/dev/null; then
    CONNECTED=true
    ok "Network reachable after ~$((i*5)) seconds"
    break
  fi
  sleep 5
done
if ! $CONNECTED; then
  warn "No internet — some steps (apt, pip) may fail. Continuing anyway."
  warn "Fix WiFi and re-run: sudo bash ${HICS_DIR}/setup.sh"
fi

# ── Step 3: Configure WiFi via NetworkManager (more reliable than wpa_supplicant) ──
step "WiFi (NetworkManager)"
WIFI_ENV="${BOOT_DIR}/hics-wifi.env"
if [[ -f "$WIFI_ENV" ]]; then
  source "$WIFI_ENV"
  if [[ -n "${WIFI_SSID:-}" ]]; then
    nmcli device wifi connect "${WIFI_SSID}" password "${WIFI_PASSWORD:-}" 2>/dev/null && \
      ok "WiFi connected: $WIFI_SSID" || \
      warn "nmcli WiFi connect failed — wpa_supplicant.conf may have already worked"
    # Remove env file so credentials don't persist unnecessarily
    rm -f "$WIFI_ENV"
  fi
else
  ok "No hics-wifi.env — assuming WiFi already configured"
fi

# ── Step 4: System packages ───────────────────────────────────────────────────
step "System packages"
if $CONNECTED; then
  apt-get update -qq 2>/dev/null && ok "apt update" || warn "apt update failed"
  PKGS=(python3-pip python3-dev git i2c-tools python3-smbus python3-pil
        libcamera-apps rpicam-apps sqlite3 ntpdate)
  apt-get install -y -q "${PKGS[@]}" 2>/dev/null && ok "apt packages installed" || warn "Some apt packages failed"
else
  warn "Skipping apt (no internet)"
fi

# ── Step 5: Python packages ───────────────────────────────────────────────────
step "Python packages (pip)"
REQ="${HICS_DIR}/requirements.txt"
if [[ -f "$REQ" ]]; then
  if $CONNECTED; then
    pip3 install --break-system-packages --quiet -r "$REQ" 2>/dev/null && \
      ok "pip packages installed" || warn "Some pip packages failed"
  else
    warn "Skipping pip (no internet)"
  fi
else
  warn "requirements.txt not found at $REQ"
fi

# ── Step 6: Enable hardware interfaces ───────────────────────────────────────
step "Hardware interfaces"
CONFIG="${BOOT_DIR}/config.txt"
[[ -f "$CONFIG" ]] || CONFIG="/boot/config.txt"

enable_param() {
  local param="$1" label="$2"
  if ! grep -q "^dtparam=${param}=on" "$CONFIG" 2>/dev/null; then
    echo "dtparam=${param}=on" >> "$CONFIG"
    ok "$label enabled"
  else
    ok "$label already enabled"
  fi
}
enable_overlay() {
  local overlay="$1" label="$2"
  if ! grep -q "^dtoverlay=${overlay}" "$CONFIG" 2>/dev/null; then
    echo "dtoverlay=${overlay}" >> "$CONFIG"
    ok "$label overlay added"
  else
    ok "$label already enabled"
  fi
}

enable_param "i2c_arm" "I2C"
enable_param "spi"     "SPI"
enable_param "w1-gpio" "1-Wire"
enable_overlay "ov5647" "Camera (OV5647)"

modprobe i2c-dev  2>/dev/null || true
modprobe w1-gpio  2>/dev/null || true

# ── Step 7: Data directory and DB path ────────────────────────────────────────
step "Data directory"
mkdir -p "$DATA_DIR"
chown pawan:pawan "$DATA_DIR"
ok "Data dir: $DATA_DIR"

CONFIG_PY="${HICS_DIR}/sensors/config.py"
if grep -q "iesh_data.db" "$CONFIG_PY" 2>/dev/null; then
  sed -i "s|DB_PATH = '.*'|DB_PATH = '${DATA_DIR}/hics.db'|" "$CONFIG_PY"
  ok "DB_PATH updated"
fi

# ── Step 8: Systemd services ──────────────────────────────────────────────────
step "Systemd services"
for svc_file in hics-core.service hics-web.service; do
  src="${HICS_DIR}/services/${svc_file}"
  dst="/etc/systemd/system/${svc_file}"
  if [[ -f "$src" ]]; then
    cp "$src" "$dst"
    ok "Installed $svc_file"
  else
    warn "$svc_file not found at $src"
  fi
done

systemctl daemon-reload 2>/dev/null || true

for svc in hics-core hics-web; do
  systemctl enable "$svc" 2>/dev/null && ok "$svc enabled" || warn "Could not enable $svc"
  systemctl start  "$svc" 2>/dev/null && ok "$svc started" || warn "$svc failed to start"
done

# ── Step 9: Disable this service ─────────────────────────────────────────────
step "Disabling firstboot service"
systemctl disable hics-firstboot 2>/dev/null || true
ok "hics-firstboot disabled (will not run again)"

# ── Step 10: Completion marker ────────────────────────────────────────────────
step "Done"
DATE_STR=$(date '+%Y-%m-%d %H:%M:%S')
echo "$DATE_STR" > "$MARKER"
chown pawan:pawan "$MARKER" 2>/dev/null || true

echo
echo "========================================================"
echo "  HICS First Boot COMPLETE — $DATE_STR"
echo "========================================================"
echo
echo "  Dashboard: http://$(hostname -I | awk '{print $1}'):5000/"
echo "  SSH:       ssh pawan@$(hostname).local"
echo "  This log:  $LOG"
echo "========================================================"

# Brief pause so the user can see if they're watching, then services take over
sleep 2
