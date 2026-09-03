"""Uploads unsynced telemetry rows to himalayansciences.org in batches.

Reads unsynced rows from the local SQLite DB, POSTs them to the HICS ingest
API, and marks them as synced on success. Runs once per upload cycle; offline
rows accumulate and are backfilled on next successful connection.

Set API_KEY in sensors/config.py with the key printed by manage.py seed_hics.
"""
import requests
import socket
import urllib.parse
from datetime import datetime, timezone

from data import database as db
from sensors.config import API_URL, API_KEY, API_NODE_ID, FIRMWARE_VERSION

BATCH_SIZE = 500
TIMEOUT    = 15  # seconds


def _online():
    """Quick TCP check before attempting the full POST.

    Uses a context manager: v0.1 leaked one file descriptor per upload cycle
    (~288/day) because the probe socket was opened and never closed.
    """
    try:
        parsed = urllib.parse.urlparse(API_URL)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        with socket.create_connection((host, port), timeout=3):
            return True
    except OSError:
        return False


def _to_utc_iso(ts):
    """Normalise a DB timestamp to the UTC ISO-8601 the ingest contract requires.

    The DB stores wall-clock local time (Asia/Kathmandu). v0.1 shipped that
    naive string straight to the API; Django rescued it by interpreting naive
    input in settings.TIME_ZONE, so stored instants were in fact correct — but
    the contract asks for UTC and that rescue is a warned, settings-dependent
    fallback. Converting here is instant-identical and removes the ambiguity.
    """
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts)
    except (TypeError, ValueError):
        return ts   # pass through unrecognised formats; server counts it as an error
    if dt.tzinfo is None:
        dt = dt.astimezone()          # attach the station's local offset
    return (dt.astimezone(timezone.utc)
              .isoformat(timespec='microseconds')
              .replace('+00:00', 'Z'))


def _round(v, places):
    """Round a sensor float, passing None through untouched."""
    return None if v is None else round(v, places)


def _row_to_reading(row: dict) -> dict:
    """Map a DB row to the wire format expected by the ingest API."""
    reading = {
        'timestamp':        _to_utc_iso(row.get('timestamp')),
        'temperature_c':    _round(row.get('air_temp'), 2),
        'humidity_rh':      _round(row.get('air_hum'), 2),
        'pressure_hpa':     _round(row.get('pressure'), 2),
        'soil_temp_c':      _round(row.get('soil_temp'), 3),
        # Reported to 2 dp: the capacitive probe's real resolution is nowhere
        # near the 17 significant figures v0.1 was sending.
        'soil_moisture_pct': _round(row.get('soil_moist'), 2),
        'firmware_version': FIRMWARE_VERSION,
    }
    module = {}
    if row.get('mq7_raw') is not None:
        module['mq7_raw'] = row['mq7_raw']
    if row.get('mq135_raw') is not None:
        module['mq135_raw'] = row['mq135_raw']
    if module:
        reading['module_data'] = module
    return reading


def upload_unsynced() -> int:
    """Upload all unsynced rows. Returns count of rows accepted, or 0 on failure.

    Drains the backlog in BATCH_SIZE chunks — if the first batch is full,
    calls itself recursively to drain remaining rows in the same cycle.
    """
    if not API_KEY:
        return 0

    if not _online():
        return 0

    rows = db.get_unsynced(limit=BATCH_SIZE)
    if not rows:
        return 0

    readings = [_row_to_reading(r) for r in rows]
    try:
        resp = requests.post(
            API_URL,
            json={'station_id': API_NODE_ID, 'readings': readings},
            headers={
                'Authorization': f'Token {API_KEY}',
                'Content-Type':  'application/json',
            },
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[Upload] Failed: {e}")
        return 0

    ids = [r['id'] for r in rows]
    db.mark_synced(ids)
    accepted = len(ids)
    print(f"[Upload] Synced {accepted} row(s).")

    # Drain remaining backlog if this batch was full
    if len(rows) == BATCH_SIZE:
        accepted += upload_unsynced()

    return accepted
