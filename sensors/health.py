"""Channel freshness + plausibility gating.

Why this exists
---------------
v0.1 held every sensor value in a variable initialised to 0.0 and overwrote it
only on a successful read. A sensor that never worked logged 0.0 forever; one
that worked and then died logged its last good value forever. Neither is
distinguishable from real data downstream — and both reached the website
(416 rows of frozen pressure, 441 rows of soil_temp 0.0, 15 rows of 85.0).

The rule now: a channel value is logged only if it is BOTH fresh (produced
within max_age seconds) and physically plausible. Otherwise the channel logs
NULL. NULL is honest; a stale number is not.

The bounds deliberately mirror ``_QUALITY_BOUNDS`` in the website's
``instruments/api.py`` — a value the server would flag ``suspect`` is not worth
sending, so we drop it at the edge. Keep the two lists in step; the ingest
contract (``docs/INGEST_CONTRACT.md``) is the shared reference.
"""
import time

# (low, high) inclusive physical bounds. Mirrors the server's _QUALITY_BOUNDS.
# Note what these already catch for free:
#   soil_temp 85.0  -> DS18B20 power-on-reset sentinel, above the 80 C ceiling
#   pressure  0.0   -> below the 300 hPa floor
BOUNDS = {
    'air_temp':   (-50.0, 60.0),
    'air_hum':    (0.0, 100.0),
    'soil_temp':  (-20.0, 80.0),
    'soil_moist': (0.0, 100.0),
    'pressure':   (300.0, 1100.0),
    'mq7_raw':    (0, 4095),
    'mq135_raw':  (0, 4095),
}

# A channel with no fresh sample within this many seconds logs NULL.
# Generous enough to ride out a few failed reads, short enough that a
# disconnected sensor stops publishing within one or two log intervals.
DEFAULT_MAX_AGE = 180.0

# Identical RAW register words in a row that mean "the register is frozen, not
# steady". A 20-bit BMP280 pressure word always dithers in its low bits; a
# bit-identical repeat this many times is a chip that reset into sleep mode
# holding old data. Only applied when the caller passes ``raw`` — a compensated
# or low-resolution value (DS18B20 at 0.0625 C, DHT22 at 0.1 C/0.1 %) repeats
# legitimately for minutes in still conditions and must never be called frozen.
FROZEN_REPEATS = 10


class Channel:
    """One logged quantity: last value, when it arrived, and whether to trust it."""

    __slots__ = ('name', 'max_age', '_value', '_stamp', '_last_raw',
                 '_repeats', 'frozen')

    def __init__(self, name, max_age=DEFAULT_MAX_AGE):
        self.name     = name
        self.max_age  = max_age
        self._value   = None
        self._stamp   = 0.0
        self._last_raw = object()   # sentinel that equals nothing
        self._repeats = 0
        self.frozen   = False

    # ── writing ──────────────────────────────────────────────────────────────
    def update(self, value, raw=None):
        """Record a reading. None (a failed read) is ignored, not stored —
        the channel simply ages out and starts logging NULL."""
        if value is None:
            return
        lo, hi = BOUNDS.get(self.name, (float('-inf'), float('inf')))
        if not (lo <= value <= hi):
            return   # implausible: treat exactly like a failed read

        # Frozen-register detection, ONLY on a pre-compensation raw word the
        # caller supplies. Without one there is nothing to judge: a steady
        # low-resolution sensor repeats bit-identically for long stretches
        # (soil at 0.0625 C steps, DHT22 at 0.1 steps, a 12-bit ADC in dry
        # soil) and would be gated to NULL for being, in fact, steady.
        if raw is not None:
            if raw == self._last_raw:
                self._repeats += 1
                if self._repeats >= FROZEN_REPEATS:
                    self.frozen = True
                    return   # stop accepting a value the chip is no longer updating
            else:
                self._last_raw = raw
                self._repeats  = 0
                self.frozen    = False

        self._value = value
        self._stamp = time.monotonic()

    # ── reading ──────────────────────────────────────────────────────────────
    @property
    def fresh(self):
        return (self._value is not None
                and (time.monotonic() - self._stamp) <= self.max_age)

    def for_log(self):
        """The value to write to the DB: the reading, or None if not trustworthy.

        A frozen channel returns None even though its last value is recent —
        detecting a stuck register is pointless if the stuck number still gets
        logged.
        """
        if self.frozen or not self.fresh:
            return None
        return self._value

    def for_display(self, default=0.0):
        """The value to draw on the OLED. Falls back so the screen never crashes;
        pair it with `state` so a stale reading is visibly marked."""
        v = self.for_log()
        return default if v is None else v

    @property
    def state(self):
        if self.frozen:
            return 'frozen'
        if self._value is None:
            return 'dead'
        return 'ok' if self.fresh else 'stale'


class ChannelSet:
    """The station's logged channels, addressed by name."""

    def __init__(self, names, max_age=DEFAULT_MAX_AGE):
        self._ch = {n: Channel(n, max_age) for n in names}

    def __getitem__(self, name):
        return self._ch[name]

    def update(self, name, value, raw=None):
        self._ch[name].update(value, raw)

    def row(self, names):
        """Values for a DB insert, in the given order — None where untrustworthy."""
        return [self._ch[n].for_log() for n in names]

    def unhealthy(self):
        """{name: state} for every channel that is not 'ok'. Empty dict == all good."""
        return {n: c.state for n, c in self._ch.items() if c.state != 'ok'}

    def summary(self):
        """One-line health string for the service log."""
        bad = self.unhealthy()
        if not bad:
            return 'all channels ok'
        return ' '.join(f'{n}={s}' for n, s in sorted(bad.items()))
