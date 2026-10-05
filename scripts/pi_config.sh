#!/bin/bash
# Apply the HANDOFF §11 config.txt changes on the station — idempotent.
#
#   sudo scripts/pi_config.sh --dry-run    # show the diff, change nothing
#   sudo scripts/pi_config.sh              # back up, apply, show the diff
#
# What it does (each one is a HANDOFF §11 item; re-running is harmless):
#   11.1  dtparam=i2c_arm_baudrate=100000      (was 400000 — the F2 mechanism)
#   11.2  dtoverlay=i2c-rtc,ds3231            (so /dev/rtc0 exists — F4)
#   11.3  comment out dtoverlay=ov5647        (auto-detect alone finds the OV5647 — F6)
#   F1    arm_freq=1000  dtoverlay=disable-bt (lighter peak load on the 5 V 2 A feed —
#                                             HANDOFF §0.1 / docs/rooftop-plan.html §E)
#   also  dtparam=i2c_arm=on  dtparam=spi=on  dtoverlay=w1-gpio   (must be present)
#
# It does NOT reboot, and it does NOT touch the RTC: after the reboot do
#   sudo hwclock -w && sudo hwclock -r
# with a FRESH coin cell fitted, or the DS3231 keeps reading 2000-01-05.
set -euo pipefail

CFG=/boot/firmware/config.txt
[ -f "$CFG" ] || CFG=/boot/config.txt
[ -f "$CFG" ] || { echo "no config.txt found"; exit 1; }

DRY=0; [ "${1:-}" == "--dry-run" ] && DRY=1
[ "$DRY" == 1 ] || [ "$(id -u)" == 0 ] || { echo "run with sudo (or --dry-run)"; exit 1; }

TMP=$(mktemp); cp "$CFG" "$TMP"

# ensure_line KEY=VALUE  — replace any line starting with KEY= (even commented), else append
ensure_line() {
    local key="${1%=*}" line="$1"      # everything before the LAST "=", e.g. dtparam=i2c_arm_baudrate
    if grep -qE "^[#[:space:]]*${key}=" "$TMP"; then
        sed -i -E "0,/^[#[:space:]]*${key}=.*/s//${line}/" "$TMP"
    else
        printf '\n%s\n' "$line" >> "$TMP"
    fi
}
# ensure_overlay NAME[,args] — add "dtoverlay=NAME..." if no active line for NAME exists
ensure_overlay() {
    local name="${1%%,*}"
    grep -qE "^dtoverlay=${name}(,|$)" "$TMP" || printf '\n# HICS HANDOFF §11\ndtoverlay=%s\n' "$1" >> "$TMP"
}

ensure_line  "dtparam=i2c_arm=on"
ensure_line  "dtparam=i2c_arm_baudrate=100000"          # 11.1
ensure_line  "dtparam=spi=on"
ensure_overlay "w1-gpio"
ensure_overlay "i2c-rtc,ds3231"                          # 11.2
# 11.3: keep camera_auto_detect, retire the explicit ov5647 overlay (the two conflicted)
sed -i -E 's/^(dtoverlay=ov5647.*)$/# \1   # HANDOFF §11.3: camera_auto_detect finds it/' "$TMP"
ensure_line  "camera_auto_detect=1"
# F1: the as-built 5 V 2 A feed undervolts under sustained 4-core load; trim the peak
ensure_line  "arm_freq=1000"
ensure_overlay "disable-bt"

echo "--- diff $CFG ---"
diff -u "$CFG" "$TMP" || true
echo

if [ "$DRY" == 1 ]; then
    echo "dry run: nothing written"; rm -f "$TMP"; exit 0
fi
BAK="$CFG.bak-$(date +%Y%m%d-%H%M%S)"
cp "$CFG" "$BAK"
cp "$TMP" "$CFG"; rm -f "$TMP"
echo "applied. backup at $BAK"
echo "next:  sudo systemctl disable hciuart   (Bluetooth is off now)"
echo "       sudo reboot   then   ls /dev/rtc0 && sudo hwclock -w && sudo hwclock -r"
