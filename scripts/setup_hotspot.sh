#!/bin/bash
# Sets up the dual-network configuration:
#   wlan0 (internal WiFi) → hotspot "IESH_Hub", IP 10.42.0.1
#   wlan1 (USB WiFi dongle) → connects to internet / uploads to API
#
# Run once as root. After reboot both connections come up automatically.
# Usage: sudo bash scripts/setup_hotspot.sh

set -e

SSID="IESH_Hub"
PASSWORD="iesh2024"   # change this
HOTSPOT_IFACE="wlan0"
INTERNET_IFACE="wlan1"

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
echo "  Dashboard: http://10.42.0.1:5000  (connect phone to '$SSID')"
echo "  SSH admin: ssh pawan@10.42.0.1"
echo "  Or via ethernet: ssh pawan@<rpi-ip>"
