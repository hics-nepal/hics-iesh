"""HICS web dashboard — Flask app serving live telemetry from SQLite."""
import sys
import os
import socket
import threading
import time
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, abort, send_file, Response
import data.database as db
from sensors.config import SEA_LEVEL_HPA, API_KEY
import curriculum
from sensors.camera import capture_sky, sky_analysis, stream_frames, streaming as cam_streaming, DEFAULT_PATH as SKY_PATH

app = Flask(__name__, template_folder='templates', static_folder='static')

# ── Sky camera state ────────────────────────────────────────────────────────
_sky_state = {}

def _camera_loop():
    """Background daemon: capture sky every 2 minutes, update _sky_state.
    Skips capture while MJPEG streaming is active (shared camera hardware)."""
    global _sky_state
    while True:
        if not cam_streaming.is_set():
            try:
                ok = capture_sky(SKY_PATH)
                if ok:
                    _sky_state = sky_analysis(SKY_PATH)
            except Exception:
                pass
        time.sleep(120)

_cam_thread = threading.Thread(target=_camera_loop, daemon=True, name='sky-cam')
_cam_thread.start()


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


def _mq_sensor_voltage(raw_adc):
    """Correct raw ADC value back to true MQ sensor output voltage (0–5V).
    The 2× voltage divider halves AOUT before the ADC, so we multiply back."""
    from sensors.config import MQ_DIVIDER_RATIO
    if raw_adc is None:
        return None
    return round((raw_adc / 4095) * 3.3 * MQ_DIVIDER_RATIO, 3)


def _enrich(row):
    if not row:
        return row
    r = dict(row)
    r['altitude']    = _pressure_to_altitude(r.get('pressure'))
    r['heat_index']  = _heat_index_c(r.get('air_temp'), r.get('air_hum'))
    r['mq7_voltage'] = _mq_sensor_voltage(r.get('mq7_raw'))
    r['mq135_voltage'] = _mq_sensor_voltage(r.get('mq135_raw'))
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


@app.route('/camera')
def camera_page():
    return render_template('camera.html', sky=_sky_state)


@app.route('/api/camera/latest.jpg')
def api_camera_latest():
    if not os.path.exists(SKY_PATH):
        return Response('No image yet', status=503)
    return send_file(SKY_PATH, mimetype='image/jpeg',
                     max_age=0, conditional=True)


@app.route('/api/camera/sky')
def api_camera_sky():
    return jsonify(_sky_state)


@app.route('/api/camera/stream')
def api_camera_stream():
    return Response(stream_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame',
                    headers={'Cache-Control': 'no-cache, no-store',
                             'X-Accel-Buffering': 'no'})


@app.route('/learn')
def learn_index():
    return render_template('learn/index.html', modules=curriculum.all_modules())


@app.route('/learn/<module_id>')
def learn_module(module_id):
    module = curriculum.get_module(module_id)
    if not module:
        abort(404)
    latest = _enrich(db.get_latest()) or {}
    return render_template('learn/module.html', module=module, latest=latest)


@app.route('/learn/<module_id>/<activity_id>')
def learn_activity(module_id, activity_id):
    module, activity = curriculum.get_activity(module_id, activity_id)
    if not activity:
        abort(404)
    latest = _enrich(db.get_latest()) or {}
    return render_template('learn/activity.html', module=module, activity=activity, latest=latest)


if __name__ == '__main__':
    db.init()
    app.run(host='0.0.0.0', port=5000, debug=False)
