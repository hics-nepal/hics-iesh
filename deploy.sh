#!/bin/bash
# Deploy HICS to Raspberry Pi.
# Usage:
#   ./deploy.sh                      — sync all project files
#   ./deploy.sh --file sensors/x.py  — sync one file, preserving its path
#   ./deploy.sh --restart            — sync + restart running services
#   ./deploy.sh --install            — first-time: install systemd services + enable on boot
#   ./deploy.sh --test               — sync + run full hardware test suite on RPI
#
# IMPORTANT: always use this script (or rsync -avR) to sync files.
# Never write bare rsync commands with a list of source files — rsync will
# flatten them into the destination directory and silently put them in the
# wrong place (e.g. sensors/config.py ends up as hics/config.py).

set -e

RPI="pawan@<rpi-ip>"
KEY="$HOME/.ssh/hics_rpi"
SSH="ssh -i $KEY"
RPI_DIR="/home/pawan"

echo "=== HICS Deploy ==="
echo "Target: $RPI"
echo ""

# Single-file sync — preserves directory structure via --relative
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

# Sync all project files (excluding git history and local-only files)
rsync -avz --progress \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.db' \
    --exclude='archive/' \
    -e "ssh -i $KEY" \
    ./ "$RPI:$RPI_DIR/hics/"

echo ""
echo "Files synced to $RPI:$RPI_DIR/hics/"

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
    $SSH $RPI "cd $RPI_DIR/hics && \
               sudo systemctl restart hics-core hics-web && \
               sleep 2 && \
               sudo systemctl status hics-core hics-web --no-pager -l"
fi

if [ "$1" == "--test" ]; then
    echo ""
    echo "--- Running hardware tests on RPI ---"
    $SSH $RPI "cd $RPI_DIR/hics && sudo python3 tests/test_all.py"
fi

echo ""
echo "=== Done ==="
echo ""
echo "Useful commands:"
echo "  ssh -i $KEY $RPI"
echo "  ssh -i $KEY $RPI 'cd ~/hics && sudo python3 tests/test_all.py'"
echo "  ssh -i $KEY $RPI 'sudo systemctl status hics-core hics-web'"
