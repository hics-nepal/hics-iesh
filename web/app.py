"""HICS web dashboard — Flask app serving live telemetry from SQLite."""
import sys
import os
import socket
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify
import data.database as db
from sensors.config import SEA_LEVEL_HPA, API_KEY

app = Flask(__name__, template_folder='templates')


def _pressure_to_altitude(pressure_hpa):
    if not pressure_hpa:
        return None
    return round(44330.0 * (1.0 - (pressure_hpa / SEA_LEVEL_HPA) ** 0.1903), 1)


def _heat_index_c(temp_c, humidity):
    """Steadman heat index in °C. Returns None for temp < 20°C."""
    if temp_c is None or humidity is None or temp_c < 20:
        return None
    T = temp_c * 9 / 5 + 32
    H = humidity
    HI = (-42.379 + 2.04901523 * T + 10.14333127 * H
          - 0.22475541 * T * H - 0.00683783 * T ** 2
          - 0.05481717 * H ** 2 + 0.00122874 * T ** 2 * H
          + 0.00085282 * T * H ** 2 - 0.00000199 * T ** 2 * H ** 2)
    return round((HI - 32) * 5 / 9, 1)


def _online():
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect(('8.8.8.8', 53))
        s.close()
        return True
    except Exception:
        return False


def _enrich(row):
    if not row:
        return row
    r = dict(row)
    r['altitude']   = _pressure_to_altitude(r.get('pressure'))
    r['heat_index'] = _heat_index_c(r.get('air_temp'), r.get('air_hum'))
    return r


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data')
def api_data():
    history = db.get_recent(100)
    latest  = db.get_latest()
    return jsonify({
        'latest':  _enrich(latest),
        'history': [_enrich(r) for r in history],
    })


@app.route('/api/latest')
def api_latest():
    return jsonify(_enrich(db.get_latest()) or {})


@app.route('/api/status')
def api_status():
    return jsonify({
        'online':      _online(),
        'api_key_set': bool(API_KEY),
        'db_rows':     db.count(),
        'timestamp':   datetime.now().isoformat(),
    })


if __name__ == '__main__':
    db.init()
    app.run(host='0.0.0.0', port=5000, debug=False)
