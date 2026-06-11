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

SKY_LOG_SQL = '''
    CREATE TABLE IF NOT EXISTS sky_log (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp     DATETIME NOT NULL,
        condition     TEXT,
        cloud_cover   REAL,
        brightness    INTEGER,
        r_mean        REAL,
        g_mean        REAL,
        b_mean        REAL
    )
'''

def init():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(CREATE_SQL)
        conn.execute(SKY_LOG_SQL)
        conn.execute('CREATE INDEX IF NOT EXISTS idx_ts ON telemetry(timestamp)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_sky_ts ON sky_log(timestamp)')
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


def get_recent_hours(hours=2):
    """Return all rows from the last N hours, oldest first."""
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                'SELECT * FROM telemetry WHERE timestamp >= ? ORDER BY timestamp ASC',
                (cutoff,)
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[DB] Read error: {e}")
        return []


def get_hourly_averages(hours=168):
    """Return hourly averaged rows for the last N hours, oldest first."""
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                '''SELECT
                     strftime('%Y-%m-%dT%H:00', timestamp) AS hour,
                     ROUND(AVG(air_temp),2)    AS avg_air_temp,
                     ROUND(AVG(air_hum),2)     AS avg_air_hum,
                     ROUND(AVG(soil_temp),2)   AS avg_soil_temp,
                     ROUND(AVG(soil_moist),2)  AS avg_soil_moist,
                     ROUND(AVG(pressure),2)    AS avg_pressure,
                     ROUND(AVG(mq7_raw),1)     AS avg_mq7,
                     ROUND(AVG(mq135_raw),1)   AS avg_mq135,
                     COUNT(*)                   AS cnt
                   FROM telemetry
                   WHERE timestamp >= ?
                   GROUP BY strftime('%Y-%m-%dT%H', timestamp)
                   ORDER BY hour ASC''',
                (cutoff,)
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[DB] Read error: {e}")
        return []


def get_daily_summary(days=30):
    """Return per-day min/max/avg for all sensors, newest first."""
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                '''SELECT
                     strftime('%Y-%m-%d', timestamp) AS date,
                     ROUND(MIN(air_temp),1)   AS min_air_temp,
                     ROUND(MAX(air_temp),1)   AS max_air_temp,
                     ROUND(AVG(air_temp),1)   AS avg_air_temp,
                     ROUND(MIN(air_hum),1)    AS min_air_hum,
                     ROUND(MAX(air_hum),1)    AS max_air_hum,
                     ROUND(AVG(air_hum),1)    AS avg_air_hum,
                     ROUND(MIN(soil_temp),1)  AS min_soil_temp,
                     ROUND(MAX(soil_temp),1)  AS max_soil_temp,
                     ROUND(AVG(soil_temp),1)  AS avg_soil_temp,
                     ROUND(MIN(soil_moist),1) AS min_soil_moist,
                     ROUND(MAX(soil_moist),1) AS max_soil_moist,
                     ROUND(AVG(soil_moist),1) AS avg_soil_moist,
                     ROUND(MIN(pressure),1)   AS min_pressure,
                     ROUND(MAX(pressure),1)   AS max_pressure,
                     ROUND(AVG(pressure),1)   AS avg_pressure,
                     ROUND(MIN(mq7_raw))      AS min_mq7,
                     ROUND(MAX(mq7_raw))      AS max_mq7,
                     ROUND(AVG(mq7_raw),1)    AS avg_mq7,
                     ROUND(MIN(mq135_raw))    AS min_mq135,
                     ROUND(MAX(mq135_raw))    AS max_mq135,
                     ROUND(AVG(mq135_raw),1)  AS avg_mq135,
                     COUNT(*)                  AS readings
                   FROM telemetry
                   WHERE timestamp >= ?
                   GROUP BY strftime('%Y-%m-%d', timestamp)
                   ORDER BY date DESC''',
                (cutoff,)
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[DB] Read error: {e}")
        return []


def get_sensor_stats():
    """Return current, 1h-ago, 1h/24h/all-time min/avg/max for all sensors."""
    from datetime import timedelta
    now = datetime.now()
    cut1h  = (now - timedelta(hours=1)).isoformat()
    cut24h = (now - timedelta(hours=24)).isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            # Latest values
            latest = conn.execute(
                'SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 1'
            ).fetchone()
            # Value from ~1h ago (oldest row within the 1h window)
            prev = conn.execute(
                'SELECT * FROM telemetry WHERE timestamp >= ? ORDER BY timestamp ASC LIMIT 1',
                (cut1h,)
            ).fetchone()
            # 1h aggregates
            h1 = conn.execute(
                '''SELECT
                     ROUND(MIN(air_temp),2) mi_t,  ROUND(MAX(air_temp),2) ma_t,  ROUND(AVG(air_temp),2) av_t,
                     ROUND(MIN(air_hum),2)  mi_h,  ROUND(MAX(air_hum),2)  ma_h,  ROUND(AVG(air_hum),2)  av_h,
                     ROUND(MIN(soil_temp),2) mi_st, ROUND(MAX(soil_temp),2) ma_st,ROUND(AVG(soil_temp),2) av_st,
                     ROUND(MIN(soil_moist),2) mi_sm,ROUND(MAX(soil_moist),2) ma_sm,ROUND(AVG(soil_moist),2) av_sm,
                     ROUND(MIN(pressure),2) mi_p,  ROUND(MAX(pressure),2) ma_p,  ROUND(AVG(pressure),2)  av_p,
                     ROUND(MIN(mq7_raw),1)  mi_mq7,ROUND(MAX(mq7_raw),1)  ma_mq7,ROUND(AVG(mq7_raw),1)  av_mq7,
                     ROUND(MIN(mq135_raw),1) mi_mq135,ROUND(MAX(mq135_raw),1) ma_mq135,ROUND(AVG(mq135_raw),1) av_mq135
                   FROM telemetry WHERE timestamp >= ?''',
                (cut1h,)
            ).fetchone()
            # 24h aggregates
            h24 = conn.execute(
                '''SELECT
                     ROUND(MIN(air_temp),2) mi_t,  ROUND(MAX(air_temp),2) ma_t,  ROUND(AVG(air_temp),2) av_t,
                     ROUND(MIN(air_hum),2)  mi_h,  ROUND(MAX(air_hum),2)  ma_h,  ROUND(AVG(air_hum),2)  av_h,
                     ROUND(MIN(soil_temp),2) mi_st, ROUND(MAX(soil_temp),2) ma_st,ROUND(AVG(soil_temp),2) av_st,
                     ROUND(MIN(soil_moist),2) mi_sm,ROUND(MAX(soil_moist),2) ma_sm,ROUND(AVG(soil_moist),2) av_sm,
                     ROUND(MIN(pressure),2) mi_p,  ROUND(MAX(pressure),2) ma_p,  ROUND(AVG(pressure),2)  av_p,
                     ROUND(MIN(mq7_raw),1)  mi_mq7,ROUND(MAX(mq7_raw),1)  ma_mq7,ROUND(AVG(mq7_raw),1)  av_mq7,
                     ROUND(MIN(mq135_raw),1) mi_mq135,ROUND(MAX(mq135_raw),1) ma_mq135,ROUND(AVG(mq135_raw),1) av_mq135
                   FROM telemetry WHERE timestamp >= ?''',
                (cut24h,)
            ).fetchone()
            # All-time min/max + row count
            all_ = conn.execute(
                '''SELECT
                     ROUND(MIN(air_temp),2) mi_t,  ROUND(MAX(air_temp),2) ma_t,
                     ROUND(MIN(air_hum),2)  mi_h,  ROUND(MAX(air_hum),2)  ma_h,
                     ROUND(MIN(soil_temp),2) mi_st, ROUND(MAX(soil_temp),2) ma_st,
                     ROUND(MIN(soil_moist),2) mi_sm,ROUND(MAX(soil_moist),2) ma_sm,
                     ROUND(MIN(pressure),2) mi_p,  ROUND(MAX(pressure),2) ma_p,
                     ROUND(MIN(mq7_raw),1)  mi_mq7,ROUND(MAX(mq7_raw),1)  ma_mq7,
                     ROUND(MIN(mq135_raw),1) mi_mq135,ROUND(MAX(mq135_raw),1) ma_mq135,
                     COUNT(*) total_rows
                   FROM telemetry'''
            ).fetchone()

        result = {}
        if latest:
            result.update(dict(latest))
        if prev:
            result['prev_air_temp']   = prev['air_temp']
            result['prev_air_hum']    = prev['air_hum']
            result['prev_soil_temp']  = prev['soil_temp']
            result['prev_soil_moist'] = prev['soil_moist']
            result['prev_pressure']   = prev['pressure']
        if h1:
            for k, v in dict(h1).items():
                result[f'h1_{k}'] = v
        if h24:
            for k, v in dict(h24).items():
                result[f'h24_{k}'] = v
        if all_:
            for k, v in dict(all_).items():
                result[f'all_{k}'] = v
        return result
    except Exception as e:
        print(f"[DB] Stats error: {e}")
        return {}


def log_sky(state: dict):
    """Persist a sky analysis result to sky_log."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                '''INSERT INTO sky_log
                   (timestamp, condition, cloud_cover, brightness, r_mean, g_mean, b_mean)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (datetime.now().isoformat(),
                 state.get('condition'), state.get('cloud_cover_pct'),
                 state.get('brightness'),
                 state.get('r_mean'), state.get('g_mean'), state.get('b_mean'))
            )
    except Exception as e:
        print(f"[DB] Sky log error: {e}")


def get_sky_history(hours=24):
    """Return sky_log rows for the last N hours, oldest first."""
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                '''SELECT * FROM sky_log WHERE timestamp >= ?
                   ORDER BY timestamp ASC''',
                (cutoff,)
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[DB] Sky history error: {e}")
        return []
