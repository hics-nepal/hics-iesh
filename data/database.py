"""Unified SQLite interface for HICS telemetry data.
   Both core_dash.py and web/app.py import from here — no more schema mismatch."""
import sqlite3
from datetime import datetime
from sensors.config import DB_PATH

CREATE_SQL = '''
    CREATE TABLE IF NOT EXISTS telemetry (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp   DATETIME NOT NULL,
        air_temp    REAL,
        air_hum     REAL,
        soil_temp   REAL,
        soil_moist  REAL,
        pressure    REAL,
        mq7_raw     INTEGER,
        mq135_raw   INTEGER
    )
'''

def init():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(CREATE_SQL)
        conn.commit()

def log(air_temp, air_hum, soil_temp, soil_moist, pressure, mq7_raw, mq135_raw):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                '''INSERT INTO telemetry
                   (timestamp, air_temp, air_hum, soil_temp, soil_moist, pressure, mq7_raw, mq135_raw)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (datetime.now().isoformat(), air_temp, air_hum, soil_temp,
                 soil_moist, pressure, mq7_raw, mq135_raw)
            )
    except Exception as e:
        print(f"[DB] Write error: {e}")

def get_recent(n=100):
    """Return the last n rows as a list of dicts, oldest first."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                'SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT ?', (n,)
            ).fetchall()
        return [dict(r) for r in reversed(rows)]
    except Exception as e:
        print(f"[DB] Read error: {e}")
        return []

def get_latest():
    rows = get_recent(1)
    return rows[0] if rows else None

def count():
    """Return total number of telemetry rows."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            return conn.execute('SELECT COUNT(*) FROM telemetry').fetchone()[0]
    except Exception:
        return 0
