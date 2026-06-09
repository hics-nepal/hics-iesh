#!/bin/bash
# Deploy HICS project files to Raspberry Pi
# Usage:
#   ./deploy.sh           - sync code only
#   ./deploy.sh --restart - sync code + restart both services
#   ./deploy.sh --install - first-time: install systemd services + enable on boot

RPI="pawan@<rpi-ip>"
SSH_KEY="$HOME/.ssh/hics_rpi"
SSH="ssh -i $SSH_KEY"
RSYNC="rsync -avz --progress -e 'ssh -i $SSH_KEY'"

# Files and dirs to deploy (excludes archive, systemd, tests, deploy.sh itself)
DEPLOY_FILES=(
    core_dash.py
    hics_terminal.py
    web_dash.py
    calibrate_soil.py
    sync_rtc.py
    read_temps.py
    templates/
)

echo "=== HICS Deploy ==="
echo "Target: $RPI"
echo ""

# Sync core files
for f in "${DEPLOY_FILES[@]}"; do
    if [ -e "$f" ]; then
        rsync -avz --progress -e "ssh -i $SSH_KEY" "$f" "$RPI:/home/pawan/$f"
    fi
done

if [ "$1" == "--install" ]; then
    echo ""
    echo "--- Installing systemd services ---"
    rsync -avz -e "ssh -i $SSH_KEY" systemd/ "$RPI:/tmp/hics-systemd/"
    $SSH $RPI "sudo cp /tmp/hics-systemd/hics-core.service /etc/systemd/system/ && \
               sudo cp /tmp/hics-systemd/hics-web.service  /etc/systemd/system/ && \
               sudo systemctl daemon-reload && \
               sudo systemctl enable hics-core hics-web && \
               echo 'Services installed and enabled on boot.'"
fi

if [ "$1" == "--restart" ] || [ "$1" == "--install" ]; then
    echo ""
    echo "--- Restarting services ---"
    $SSH $RPI "sudo systemctl restart hics-core hics-web && \
               sleep 1 && \
               sudo systemctl status hics-core hics-web --no-pager -l"
fi

echo ""
echo "=== Done ==="
