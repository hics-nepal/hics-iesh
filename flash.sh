#!/usr/bin/env bash
# =============================================================================
# HICS IESH — SD Card Flash Script
# =============================================================================
# Run this on your Linux development machine (NOT on the RPi).
# Flashes Raspberry Pi OS, sets up SSH/WiFi/user, copies HICS code,
# and enables auto-setup on first power-on.
#
# Usage:
#   sudo bash flash.sh [options]
#
# Options:
#   --image PATH         Path to .img or .img.xz  (default: auto-detect ~/Downloads)
#   --device DEV         SD card device            (default: /dev/sda, with confirmation)
#   --wifi-ssid SSID     WiFi network name
#   --wifi-password PW   WiFi password
#   --hostname NAME      RPi hostname              (default: hics-iesh)
#   --password PW        RPi pawan user password   (default: random, printed at end)
#   --station-id ID      Station ID for cloud sync (e.g. KTM-001) — written to sensors/config.py
#   --api-key KEY        Station API key from himalayansciences.org — written to sensors/config.py
#   --skip-code          Only flash + configure OS, skip copying HICS code
#
# Example:
#   sudo bash flash.sh --wifi-ssid "MyNetwork" --wifi-password "MyPass"
# =============================================================================

set -euo pipefail

# ── Colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
info()    { echo -e "${CYAN}[→]${NC} $*"; }
ok()      { echo -e "${GREEN}[✓]${NC} $*"; }
warn()    { echo -e "${YELLOW}[!]${NC} $*"; }
die()     { echo -e "${RED}[✗]${NC} $*" >&2; exit 1; }
section() { echo; echo -e "${BOLD}${CYAN}━━━ $* ━━━${NC}"; echo; }

# ── Defaults ──────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_PATH=""
DEVICE="/dev/sda"
WIFI_SSID=""
WIFI_PASSWORD=""
HOSTNAME_VAL="hics-iesh"
USER_PASSWORD=""
STATION_ID=""
STATION_API_KEY=""
SKIP_CODE=false
MNT_BOOT="/tmp/hics-mnt-boot"
MNT_ROOT="/tmp/hics-mnt-root"

# ── Parse arguments ───────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --image)         IMAGE_PATH="$2";     shift 2 ;;
    --device)        DEVICE="$2";         shift 2 ;;
    --wifi-ssid)     WIFI_SSID="$2";      shift 2 ;;
    --wifi-password) WIFI_PASSWORD="$2";  shift 2 ;;
    --hostname)      HOSTNAME_VAL="$2";   shift 2 ;;
    --password)      USER_PASSWORD="$2";  shift 2 ;;
    --station-id)    STATION_ID="$2";     shift 2 ;;
    --api-key)       STATION_API_KEY="$2"; shift 2 ;;
    --skip-code)     SKIP_CODE=true;      shift   ;;
    --help|-h)
      grep '^#' "$0" | grep -v '#!/' | sed 's/^# \?//' | head -25
      exit 0 ;;
    *) die "Unknown option: $1. Use --help for usage." ;;
  esac
done

# ── Must be root ──────────────────────────────────────────────────────────────
[[ $EUID -eq 0 ]] || die "Run with sudo: sudo bash flash.sh"

# ── Required tools ────────────────────────────────────────────────────────────
for cmd in dd partprobe openssl rsync lsblk; do
  command -v "$cmd" &>/dev/null || die "Required tool not found: $cmd  (install: sudo apt install $cmd)"
done
if [[ "$IMAGE_PATH" == *.xz ]] || [[ -z "$IMAGE_PATH" ]]; then
  command -v xzcat &>/dev/null || die "xzcat not found: sudo apt install xz-utils"
fi

# ── Find image ────────────────────────────────────────────────────────────────
if [[ -z "$IMAGE_PATH" ]]; then
  IMAGE_PATH=$(ls ~/Downloads/*raspios*.img.xz 2>/dev/null | head -1 \
    || ls ~/Downloads/*.img.xz 2>/dev/null | head -1 \
    || ls ~/Downloads/*.img    2>/dev/null | head -1 \
    || true)
  [[ -z "$IMAGE_PATH" ]] && die "No RPi OS image found in ~/Downloads. Use --image /path/to/file.img.xz"
fi
[[ -f "$IMAGE_PATH" ]] || die "Image file not found: $IMAGE_PATH"

# ── Prompt for WiFi if needed ─────────────────────────────────────────────────
if [[ -z "$WIFI_SSID" ]]; then
  echo -en "${YELLOW}[?]${NC} WiFi SSID (leave blank to skip): "
  read -r WIFI_SSID
fi
if [[ -n "$WIFI_SSID" && -z "$WIFI_PASSWORD" ]]; then
  echo -en "${YELLOW}[?]${NC} WiFi password for '${WIFI_SSID}': "
  read -rs WIFI_PASSWORD; echo
fi

# ── Per-device user password (never ship a shared default) ───────────────────
PASSWORD_GENERATED=false
if [[ -z "$USER_PASSWORD" ]]; then
  USER_PASSWORD="$(tr -dc 'a-z0-9' < /dev/urandom | head -c 12)"
  PASSWORD_GENERATED=true
fi

# ── Banner ────────────────────────────────────────────────────────────────────
echo
echo -e "${BOLD}╔══════════════════════════════════════════╗"
echo -e "║    HICS IESH — SD Card Flash             ║"
echo -e "╚══════════════════════════════════════════╝${NC}"
info "Image:     $(basename "$IMAGE_PATH")  ($(du -sh "$IMAGE_PATH" | cut -f1) compressed)"
info "Device:    $DEVICE"
info "Hostname:  $HOSTNAME_VAL"
info "User:      pawan / $USER_PASSWORD$( $PASSWORD_GENERATED && echo ' (generated — note it down)')"
info "WiFi:      ${WIFI_SSID:-'(not configured)'}"
info "Station:   ${STATION_ID:-'(no cloud sync configured)'}"
info "Copy code: $( $SKIP_CODE && echo 'no (--skip-code)' || echo 'yes')"

# ── Safety: refuse internal/NVMe drives ──────────────────────────────────────
ROOT_DEV=$(lsblk -no PKNAME "$(findmnt -n -o SOURCE /)" 2>/dev/null || true)
[[ -n "$ROOT_DEV" && "/dev/$ROOT_DEV" == "$DEVICE" ]] && \
  die "ABORT: $DEVICE is your system disk! Specify the SD card with --device."
[[ "$DEVICE" == *nvme* ]] && \
  die "ABORT: $DEVICE looks like an NVMe drive. SD cards are usually /dev/sda or /dev/mmcblk0."

# Show target device and ask for explicit confirmation
echo
info "Target device:"
lsblk -o NAME,SIZE,MODEL,MOUNTPOINT "$DEVICE" 2>/dev/null || lsblk "$DEVICE"
echo
echo -e "${RED}${BOLD}  ⚠  ALL DATA on $DEVICE will be permanently erased. ⚠${NC}"
echo -en "${YELLOW}[?]${NC} Type ${BOLD}yes${NC} to continue, anything else to abort: "
read -r CONFIRM
[[ "$CONFIRM" == "yes" ]] || die "Aborted — no changes made."

# ── Step 1: Unmount ───────────────────────────────────────────────────────────
section "1/6  Unmounting $DEVICE"
for part in "${DEVICE}1" "${DEVICE}2" "${DEVICE}p1" "${DEVICE}p2"; do
  [[ -b "$part" ]] || continue
  MPOINTS=$(lsblk -no MOUNTPOINT "$part" 2>/dev/null || true)
  while IFS= read -r mp; do
    [[ -z "$mp" ]] && continue
    umount "$mp" 2>/dev/null && ok "Unmounted $mp" || true
  done <<< "$MPOINTS"
done
sync; ok "Device unmounted"

# ── Step 2: Flash ─────────────────────────────────────────────────────────────
section "2/6  Flashing (~3 minutes)"
info "Writing image to $DEVICE..."
if [[ "$IMAGE_PATH" == *.xz ]]; then
  xzcat "$IMAGE_PATH" | dd of="$DEVICE" bs=4M status=progress oflag=sync conv=fsync
else
  dd if="$IMAGE_PATH" of="$DEVICE" bs=4M status=progress oflag=sync conv=fsync
fi
sync
info "Refreshing partition table..."
partprobe "$DEVICE" 2>/dev/null || true
sleep 4   # wait for kernel to register new partitions

# Unmount anything auto-mounted by the desktop
for part in "${DEVICE}1" "${DEVICE}2"; do
  [[ -b "$part" ]] || continue
  while IFS= read -r mp; do
    [[ -z "$mp" ]] && continue
    umount "$mp" 2>/dev/null || true
  done < <(lsblk -no MOUNTPOINT "$part" 2>/dev/null || true)
done

ok "Flash complete"
lsblk "$DEVICE"

# ── Determine partition names (sda1/sda2 vs mmcblk0p1/p2) ────────────────────
if [[ -b "${DEVICE}1" ]]; then
  PART_BOOT="${DEVICE}1"
  PART_ROOT="${DEVICE}2"
elif [[ -b "${DEVICE}p1" ]]; then
  PART_BOOT="${DEVICE}p1"
  PART_ROOT="${DEVICE}p2"
else
  die "Cannot find partitions on $DEVICE — try: partprobe $DEVICE"
fi

# ── Step 3: Mount ─────────────────────────────────────────────────────────────
section "3/6  Mounting partitions"
mkdir -p "$MNT_BOOT" "$MNT_ROOT"

mount "$PART_BOOT" "$MNT_BOOT" || die "Failed to mount boot partition $PART_BOOT"
ok "Boot: $PART_BOOT → $MNT_BOOT"

if ! $SKIP_CODE; then
  mount "$PART_ROOT" "$MNT_ROOT" || die "Failed to mount root partition $PART_ROOT"
  ok "Root: $PART_ROOT → $MNT_ROOT"
fi

# ── Step 4: Configure boot partition ─────────────────────────────────────────
section "4/6  Configuring"

# Enable SSH
touch "$MNT_BOOT/ssh"
ok "SSH enabled"

# Create pawan user with hashed password
PW_HASH=$(openssl passwd -6 "$USER_PASSWORD")
echo "pawan:${PW_HASH}" > "$MNT_BOOT/userconf.txt"
ok "User 'pawan' created (password: $USER_PASSWORD)"

# WiFi — wpa_supplicant.conf (legacy but works on most RPi OS versions)
if [[ -n "$WIFI_SSID" ]]; then
  cat > "$MNT_BOOT/wpa_supplicant.conf" <<WPAEOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=NP

network={
    ssid="${WIFI_SSID}"
    psk="${WIFI_PASSWORD}"
    key_mgmt=WPA-PSK
    priority=1
}
WPAEOF
  # Also store plaintext for firstboot.sh to create NetworkManager connection
  printf 'WIFI_SSID=%s\nWIFI_PASSWORD=%s\n' "$WIFI_SSID" "$WIFI_PASSWORD" \
    > "$MNT_BOOT/hics-wifi.env"
  chmod 600 "$MNT_BOOT/hics-wifi.env"
  ok "WiFi configured: $WIFI_SSID"
fi

# Store hostname for firstboot.sh to apply
echo "$HOSTNAME_VAL" > "$MNT_BOOT/hics-hostname.txt"
ok "Hostname: $HOSTNAME_VAL"

# Embed the firstboot script in boot partition (accessible as /boot/firmware/ on RPi)
if [[ -f "${SCRIPT_DIR}/scripts/firstboot.sh" ]]; then
  install -m 755 "${SCRIPT_DIR}/scripts/firstboot.sh" "$MNT_BOOT/hics-firstboot.sh"
  ok "Firstboot script embedded in boot partition"
else
  warn "scripts/firstboot.sh not found — first-boot auto-setup will not run"
fi

# ── Step 5: Copy HICS code to rootfs ─────────────────────────────────────────
if ! $SKIP_CODE; then
  section "5/6  Copying HICS code to rootfs"

  DEST="${MNT_ROOT}/home/pawan/hics"
  mkdir -p "$DEST"
  mkdir -p "${MNT_ROOT}/home/pawan/hics-data"

  rsync -a --delete \
    --exclude='.git/' \
    --exclude='archive/' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    --exclude='.firstboot-complete' \
    --exclude='hics-firstboot.log' \
    --exclude='flash.sh' \
    "${SCRIPT_DIR}/" "${DEST}/"

  # Fix DB_PATH to correct location
  sed -i "s|DB_PATH = '.*'|DB_PATH = '/home/pawan/hics-data/hics.db'|" \
    "${DEST}/sensors/config.py" 2>/dev/null || true

  # Provision station identity for cloud sync (fleet: one flash = one configured device)
  if [[ -n "$STATION_ID" ]]; then
    sed -i "s|API_NODE_ID = '.*'|API_NODE_ID = '${STATION_ID}'|" \
      "${DEST}/sensors/config.py" 2>/dev/null || true
    ok "Station ID: $STATION_ID"
  fi
  if [[ -n "$STATION_API_KEY" ]]; then
    sed -i "s|API_KEY     = '.*'|API_KEY     = '${STATION_API_KEY}'|" \
      "${DEST}/sensors/config.py" 2>/dev/null || true
    ok "Station API key written to sensors/config.py"
  fi

  # Set ownership (uid/gid 1000 = first user on RPi OS)
  chown -R 1000:1000 "${MNT_ROOT}/home/pawan/"

  # Install firstboot service into systemd
  cp "${SCRIPT_DIR}/services/hics-firstboot.service" \
     "${MNT_ROOT}/etc/systemd/system/hics-firstboot.service" 2>/dev/null || \
     warn "Could not install hics-firstboot.service (services/ dir missing?)"

  # Enable firstboot service (create the wants symlink)
  WANTS="${MNT_ROOT}/etc/systemd/system/multi-user.target.wants"
  mkdir -p "$WANTS"
  ln -sf "/etc/systemd/system/hics-firstboot.service" \
         "${WANTS}/hics-firstboot.service" 2>/dev/null || true

  ok "Code: $(du -sh "$DEST" | cut -f1)  at $DEST"
  ok "Firstboot service enabled"
else
  section "5/6  Skipped code copy (--skip-code)"
  warn "SSH into the RPi and run: scp -r /path/to/hics pawan@<ip>:~/hics && sudo bash ~/hics/setup.sh"
fi

# ── Step 6: Unmount and sync ──────────────────────────────────────────────────
section "6/6  Finalising"
sync
umount "$MNT_BOOT" && ok "Boot partition unmounted"
if ! $SKIP_CODE && mountpoint -q "$MNT_ROOT"; then
  umount "$MNT_ROOT" && ok "Root partition unmounted"
fi
sync
rmdir "$MNT_BOOT" "$MNT_ROOT" 2>/dev/null || true

# ── Done ──────────────────────────────────────────────────────────────────────
echo
echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════════╗"
echo -e "║   ✓  SD card ready — safe to remove               ║"
echo -e "╚══════════════════════════════════════════════════════╝${NC}"
echo
echo -e "  ${BOLD}Next steps:${NC}"
echo -e "  1. Remove SD card, insert into Raspberry Pi, connect power"
echo -e "  2. First boot auto-configures everything — takes ${YELLOW}5–10 min${NC}"
echo -e "  3. Find the RPi:    ${CYAN}ping ${HOSTNAME_VAL}.local${NC}  or check your router"
echo -e "  4. SSH in:          ${CYAN}ssh pawan@${HOSTNAME_VAL}.local${NC}  (password: ${USER_PASSWORD}$( $PASSWORD_GENERATED && echo ' — generated, note it down'))"
echo -e "  5. Dashboard:       ${CYAN}http://${HOSTNAME_VAL}.local:5000/${NC}"
echo
echo -e "  First-boot log:     ${CYAN}cat ~/hics-firstboot.log${NC}"
echo -e "  Service status:     ${CYAN}sudo systemctl status hics-core hics-web${NC}"
echo
