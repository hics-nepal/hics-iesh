#!/bin/bash
# Push local code changes to a Raspberry Pi over LAN.
#
# TWO UPDATE PATHS — use the right one:
#
#   deploy.sh   — rsync from your laptop to the Pi. Use this when you are
#                 actively iterating on hardware code and need a fast loop
#                 without committing. Requires LAN access to the Pi.
#
#   git pull    — on the Pi itself, pulls from github.com/hics-nepal/hics-iesh.
#                 Use this for any code that has been committed and pushed.
#                 Works over any internet connection, no laptop needed.
#
# For a normal release cycle: commit → push → git pull on Pi.
# Use deploy.sh only during local hardware development sessions.
#
# Usage:
#   ./deploy.sh                      — sync all project files
#   ./deploy.sh --file sensors/x.py  — sync one file, preserving its path
#   ./deploy.sh --restart            — sync + restart running services
#   ./deploy.sh --pull               — git pull on Pi + restart (no local sync)
#   ./deploy.sh --install            — first-time: install systemd services + enable on boot
#   ./deploy.sh --test               — sync + run full hardware test suite on Pi
#
# Target Pi: defaults to mDNS hostname; override per-device with:
#   IESH_RPI=pawan@192.168.10.183 ./deploy.sh
#
# SSH key: defaults to ~/.ssh/hics_rpi; override with:
#   IESH_SSH_KEY=~/.ssh/id_ed25519 ./deploy.sh
#
# IMPORTANT: always use this script (or rsync -avR) to sync files.
# Never write bare rsync commands with a list of source files — rsync will
# flatten them into the destination directory and silently put them in the
# wrong place (e.g. sensors/config.py ends up as hics/config.py).

set -e

RPI="${IESH_RPI:-pawan@iesh.local}"
KEY="${IESH_SSH_KEY:-$HOME/.ssh/hics_rpi}"
SSH="ssh -i $KEY"
RPI_DIR="/home/pawan"

echo "=== HICS Deploy ==="
echo "Target: $RPI"
echo ""

# --pull: update from GitHub on the Pi, no local rsync
if [ "$1" == "--pull" ]; then
    echo "--- Pulling from GitHub on Pi ---"
    $SSH $RPI "cd $RPI_DIR/hics && git pull origin master"
    echo ""
    echo "--- Restarting services ---"
    $SSH $RPI "sudo systemctl restart hics-core hics-web && \
               sleep 2 && \
               sudo systemctl status hics-core hics-web --no-pager -l"
    exit 0
fi

# --file: single-file sync — preserves directory structure via --relative.
# Note: sensors/config.py is intentionally excluded from full syncs (it holds
# the device API key, which differs per device and is never in git). You CAN
# sync it explicitly with --file if you know what you are doing.
if [ "$1" == "--file" ]; then
    if [ -z "$2" ]; then
        echo "Usage: ./deploy.sh --file path/relative/to/project/root.py"
        exit 1
    fi
    echo "Syncing: $2"
    rsync -avz --relative -e "ssh -i $KEY" "$2" "$RPI:$RPI_DIR/hics/"
    echo "Done: $RPI:$RPI_DIR/hics/$2"
    exit 0
fi

# Full sync — push all tracked project files to the Pi.
#
# --delete removes files from ~/hics that were deleted locally, so stale
# modules can't ghost on the Pi and shadow imports. Excluded paths are
# never deleted on the remote, even with --delete.
#
# sensors/config.py is EXCLUDED — it holds the device API key and is managed
# independently on each device. Syncing it would silently wipe the key with
# the empty placeholder from the repo. The Pi keeps its own copy forever;
# git update-index --assume-unchanged keeps it out of git status.
rsync -avz --progress --delete \
    --exclude='.git' \
    --exclude='.claude/' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.db' \
    --exclude='archive/' \
    --exclude='*.log' \
    --exclude='.firstboot*' \
    --exclude='sensors/config.py' \
    -e "ssh -i $KEY" \
    ./ "$RPI:$RPI_DIR/hics/"

echo ""
echo "Files synced to $RPI:$RPI_DIR/hics/"
echo "(sensors/config.py intentionally skipped — API key managed on device)"

if [ "$1" == "--install" ]; then
    echo ""
    echo "--- Installing systemd services ---"
    $SSH $RPI "sudo cp $RPI_DIR/hics/services/hics-core.service /etc/systemd/system/ && \
               sudo cp $RPI_DIR/hics/services/hics-web.service  /etc/systemd/system/ && \
               sudo systemctl daemon-reload && \
               sudo systemctl enable hics-core hics-web && \
               echo 'Services installed and enabled on boot.'"
fi

if [ "$1" == "--restart" ] || [ "$1" == "--install" ]; then
    echo ""
    echo "--- Restarting services ---"
    $SSH $RPI "sudo systemctl restart hics-core hics-web && \
               sleep 2 && \
               sudo systemctl status hics-core hics-web --no-pager -l"
fi

if [ "$1" == "--test" ]; then
    echo ""
    echo "--- Running hardware tests on Pi ---"
    $SSH $RPI "cd $RPI_DIR/hics && sudo python3 tests/test_all.py"
fi

echo ""
echo "=== Done ==="
echo ""
echo "Useful commands:"
echo "  ssh -i $KEY $RPI"
echo "  ssh -i $KEY $RPI 'cd ~/hics && sudo python3 tests/test_all.py'"
echo "  ssh -i $KEY $RPI 'sudo systemctl status hics-core hics-web'"
