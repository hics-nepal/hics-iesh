"""Uploads telemetry to himalayansciences.org/data/api/ when internet is available.
   Set API_KEY in sensors/config.py once you have credentials from the site."""
import requests
import socket
from sensors.config import API_URL, API_KEY, API_NODE_ID

TIMEOUT = 10  # seconds

def _online():
    """Quick connectivity check — tries to reach the API host."""
    try:
        host = API_URL.split('/')[2]
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, 443))
        return True
    except Exception:
        return False

def upload(row: dict) -> bool:
    """POST one telemetry row to the API. Returns True on success.

    row should contain: timestamp, air_temp, air_hum, soil_temp,
                        soil_moist, pressure, mq7_raw, mq135_raw
    """
    if not API_KEY:
        return False   # Not configured yet

    if not _online():
        return False

    payload = {
        'node_id':    API_NODE_ID,
        'timestamp':  row.get('timestamp'),
        'air_temp':   row.get('air_temp'),
        'air_hum':    row.get('air_hum'),
        'soil_temp':  row.get('soil_temp'),
        'soil_moist': row.get('soil_moist'),
        'pressure':   row.get('pressure'),
        'mq7_raw':    row.get('mq7_raw'),
        'mq135_raw':  row.get('mq135_raw'),
    }

    try:
        resp = requests.post(
            API_URL,
            json=payload,
            headers={'Authorization': f'Bearer {API_KEY}'},
            timeout=TIMEOUT
        )
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[Upload] Failed: {e}")
        return False
