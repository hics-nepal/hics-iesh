import glob
import os
import subprocess
from .config import DS18B20_BASE_DIR

# The DS18B20 writes 0x0550 (= 85.0 C) into its scratchpad on power-up and
# keeps it there until the first conversion completes. On this station it is a
# brownout signature, not a temperature — 15 rows of 85.0 reached the website
# before it was gated. Rejected here as well as by sensors.health BOUNDS.
POR_SENTINEL = 85.0


class DS18B20:
    """1-Wire soil temperature probe.

    Rescans the bus on every failed read. The probe on this station drops off
    the bus under undervoltage and comes back (observed: absent, then
    28-062261761e24 present minutes later) — v0.1 latched ok=False at init and
    stayed dead until the service was restarted.
    """

    def __init__(self):
        self.ok = False
        self.error = None
        self._device_file = None
        self._load_modules()
        self._scan()

    @staticmethod
    def _load_modules():
        # Loaded by dtoverlay=w1-gpio in normal operation; this is belt-and-braces.
        # v0.1 used os.system('modprobe ...'), which printed "modprobe: not found"
        # because /usr/sbin is not on a login user's PATH.
        for mod in ('w1-gpio', 'w1-therm'):
            try:
                subprocess.run(['/usr/sbin/modprobe', mod],
                               check=False, capture_output=True, timeout=5)
            except (OSError, subprocess.SubprocessError):
                pass

    def _scan(self):
        """Look for a 28-* device on the bus. Returns True if one is present."""
        try:
            folders = sorted(glob.glob(os.path.join(DS18B20_BASE_DIR, '28*')))
            if not folders:
                self._device_file = None
                self.ok = False
                self.error = 'No DS18B20 found on 1-Wire bus'
                return False
            self._device_file = os.path.join(folders[0], 'w1_slave')
            self.ok = True
            self.error = None
            return True
        except OSError as e:
            self._device_file = None
            self.ok = False
            self.error = str(e)
            return False

    def read(self):
        """Temperature in C, or None. None on: absent probe, CRC failure, or the
        85.0 power-on-reset sentinel."""
        if not self.ok and not self._scan():
            return None
        try:
            with open(self._device_file, 'r') as f:
                lines = f.readlines()
        except OSError as e:
            # Probe vanished mid-read — drop it and rescan on the next call.
            self.error = str(e)
            self.ok = False
            self._device_file = None
            return None

        if len(lines) < 2 or lines[0].strip()[-3:] != 'YES':
            self.error = 'CRC failure'
            return None
        pos = lines[1].find('t=')
        if pos == -1:
            self.error = 'no t= field'
            return None
        try:
            temp = float(lines[1][pos + 2:]) / 1000.0
        except ValueError:
            self.error = 'unparseable t= field'
            return None

        if temp == POR_SENTINEL:
            self.error = 'power-on-reset sentinel (85.0) — check supply'
            return None
        self.error = None
        return temp
