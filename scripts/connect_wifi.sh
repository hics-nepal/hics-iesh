#!/bin/bash
# Connect the USB WiFi adapter (wlan1) to the internet.
# Credentials are stored in NetworkManager and persist across reboots.
# Usage: sudo bash scripts/connect_wifi.sh [SSID] [PASSWORD]

IFACE="wlan1"
SSID="${1:-}"
PASS="${2:-}"

if [ -z "$SSID" ]; then
    read -rp "WiFi SSID: " SSID
fi
if [ -z "$PASS" ]; then
    read -rsp "WiFi password for '$SSID': " PASS; echo
fi

if ! ip link show "$IFACE" &>/dev/null; then
    echo "ERROR: $IFACE not found."
    echo "  Is the USB WiFi adapter plugged in?"
    echo "  Available interfaces: $(ip -o link | awk -F': ' '{print $2}' | grep -v lo | tr '\n' ' ')"
    exit 1
fi

echo "Scanning for '$SSID' on $IFACE..."
nmcli dev wifi rescan ifname "$IFACE" 2>/dev/null || true
sleep 2

echo "Connecting $IFACE to '$SSID'..."
nmcli dev wifi connect "$SSID" password "$PASS" ifname "$IFACE"

if [ $? -eq 0 ]; then
    IP=$(ip -4 addr show "$IFACE" 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    echo ""
    echo "OK — $IFACE connected to '$SSID'"
    echo "  IP address : ${IP:-<dhcp pending>}"
    echo "  Test: ping -I $IFACE 8.8.8.8 -c 3"
else
    echo ""
    echo "FAILED to connect. Troubleshoot:"
    echo "  List visible networks : nmcli dev wifi list ifname $IFACE"
    echo "  Show saved connections : nmcli con show"
    echo "  Manual scan            : nmcli dev wifi rescan ifname $IFACE"
fi
