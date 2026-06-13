"""Uploads unsynced telemetry rows to himalayansciences.org in batches.

Reads unsynced rows from the local SQLite DB, POSTs them to the HICS ingest
API, and marks them as synced on success. Runs once per upload cycle; offline
rows accumulate and are backfilled on next successful connection.

Set API_KEY in sensors/config.py with the key printed by manage.py seed_hics.
"""
import requests
import socket
import urllib.parse
from data import database as db
from sensors.config import API_URL, API_KEY, API_NODE_ID, FIRMWARE_VERSION

BATCH_SIZE = 500
TIMEOUT    = 15  # seconds


def _online():
    """Quick TCP check before attempting the full POST."""
    try:
        parsed = urllib.parse.urlparse(API_URL)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        af   = socket.AF_INET
        socket.setdefaulttimeout(3)
        socket.socket(af, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def _row_to_reading(row: dict) -> dict:
    """Map a DB row to the wire format expected by the ingest API."""
    reading = {
        'timestamp':        row.get('timestamp'),
        'temperature_c':    row.get('air_temp'),
        'humidity_rh':      row.get('air_hum'),
        'pressure_hpa':     row.get('pressure'),
        'soil_temp_c':      row.get('soil_temp'),
        'soil_moisture_pct': row.get('soil_moist'),
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
