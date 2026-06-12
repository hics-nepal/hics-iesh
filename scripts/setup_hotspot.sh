#!/bin/bash
# Sets up the dual-network configuration:
#   wlan0 (internal WiFi) → hotspot "IESH_Hub", IP 10.42.0.1
#   wlan1 (USB WiFi dongle) → connects to internet / uploads to API
#
# Run once as root. After reboot both connections come up automatically.
# Usage: sudo bash scripts/setup_hotspot.sh [HOTSPOT_PASSWORD]
#
# If no password is given, a random per-device one is generated, printed once,
# and saved to /home/pawan/hics-data/hotspot_password.txt (root-readable file
# on the device itself — write it on the station's label).

set -e

SSID="IESH_Hub"
PASSWORD="${1:-}"
HOTSPOT_IFACE="wlan0"
INTERNET_IFACE="wlan1"

PASS_FILE="/home/pawan/hics-data/hotspot_password.txt"
if [ -z "$PASSWORD" ]; then
    if [ -f "$PASS_FILE" ]; then
        PASSWORD="$(cat "$PASS_FILE")"
        echo "Reusing existing hotspot password from $PASS_FILE"
    else
        PASSWORD="$(tr -dc 'a-z0-9' < /dev/urandom | head -c 10)"
        echo "Generated random hotspot password (no argument given)."
    fi
fi
mkdir -p "$(dirname "$PASS_FILE")"
printf '%s\n' "$PASSWORD" > "$PASS_FILE"
chmod 600 "$PASS_FILE"

echo "=== HICS Network Setup ==="

# ── 1. Create the Wi-Fi hotspot on wlan0 ─────────────────────────────────────
echo "[1/3] Creating hotspot on $HOTSPOT_IFACE ..."
nmcli con delete "IESH_Hotspot" 2>/dev/null || true
nmcli con add type wifi ifname $HOTSPOT_IFACE con-name IESH_Hotspot ssid "$SSID" \
    mode ap 802-11-wireless.band bg
nmcli con modify IESH_Hotspot \
    ipv4.method shared \
    ipv4.addresses 10.42.0.1/24 \
    wifi-sec.key-mgmt wpa-psk \
    wifi-sec.psk "$PASSWORD"
nmcli con up IESH_Hotspot
echo "  Hotspot SSID: $SSID  Password: $PASSWORD  IP: 10.42.0.1"

# ── 2. If USB WiFi adapter is present, connect it to internet ────────────────
if ip link show $INTERNET_IFACE &>/dev/null; then
    echo "[2/3] $INTERNET_IFACE found — connecting to internet WiFi..."
    bash "$(dirname "$0")/connect_wifi.sh" || true
else
    echo "[2/3] $INTERNET_IFACE not found — plug in USB WiFi adapter, then run:"
    echo "      sudo bash scripts/connect_wifi.sh"
fi

# ── 3. Make sure HICS services start on boot ─────────────────────────────────
echo "[3/3] Enabling HICS systemd services ..."
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
sudo cp "$SCRIPT_DIR/services/hics-core.service" /etc/systemd/system/
sudo cp "$SCRIPT_DIR/services/hics-web.service"  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hics-core hics-web
sudo systemctl restart hics-core hics-web

echo ""
echo "=== Done ==="
echo "  Hotspot:   $SSID  password: $PASSWORD  (also saved to $PASS_FILE)"
echo "  Dashboard: http://10.42.0.1:5000  (connect phone to '$SSID')"
echo "  SSH admin: ssh pawan@10.42.0.1"
