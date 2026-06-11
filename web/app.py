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
from sensors import air_quality

app = Flask(__name__, template_folder='templates', static_folder='static')
db.init()

# ── Sky camera state ────────────────────────────────────────────────────────
_sky_state = {}

def _camera_loop():
    """Background daemon: capture sky every 15 minutes, update _sky_state.
    Skips capture while MJPEG streaming is active (shared camera hardware)."""
    global _sky_state
    while True:
        if not cam_streaming.is_set():
            try:
                ok = capture_sky(SKY_PATH)
                if ok:
                    _sky_state = sky_analysis(SKY_PATH)
                    db.log_sky(_sky_state)
            except Exception:
                pass
        time.sleep(900)

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


def _mq_rs(raw_adc):
    """Sensor resistance RS (Ω) from a logged raw ADC value."""
    from sensors.config import MQ_VCC, MQ_RL_OHM
    v = _mq_sensor_voltage(raw_adc)
    if not v or v < 0.01:
        return None
    return MQ_RL_OHM * (MQ_VCC / v - 1.0)


def _enrich(row):
    if not row:
        return row
    r = dict(row)
    r['altitude']    = _pressure_to_altitude(r.get('pressure'))
    r['heat_index']  = _heat_index_c(r.get('air_temp'), r.get('air_hum'))
    r['mq7_voltage'] = _mq_sensor_voltage(r.get('mq7_raw'))
    r['mq135_voltage'] = _mq_sensor_voltage(r.get('mq135_raw'))
    aqi = air_quality.proxy_aqi(_mq_rs(r.get('mq7_raw')),
                                _mq_rs(r.get('mq135_raw')))
    if aqi:
        r['aqi']          = aqi['aqi']
        r['aqi_category'] = aqi['category']
        r['co_ppm']       = aqi['co_ppm']
        r['co2eq_ppm']    = aqi['co2eq_ppm']
    return r


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data')
def api_data():
    from flask import request as req
    hours = req.args.get('hours', type=int)
    if hours:
        history = db.get_recent_hours(min(max(hours, 1), 168))
    else:
        history = db.get_recent(100)
    latest = db.get_latest()
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


@app.route('/history')
def history_page():
    return render_template('history.html')


@app.route('/api/history')
def api_history():
    from flask import request as req
    hours = req.args.get('hours', 168, type=int)
    hours = min(max(hours, 1), 720)
    if hours <= 6:
        rows = db.get_recent_hours(hours)
        data = [_enrich(r) for r in rows]
        mode = 'raw'
    else:
        data = db.get_hourly_averages(hours)
        mode = 'hourly'
    return jsonify({'mode': mode, 'hours': hours, 'data': data})


@app.route('/api/daily')
def api_daily():
    from flask import request as req
    days = req.args.get('days', 30, type=int)
    days = min(max(days, 1), 365)
    return jsonify(db.get_daily_summary(days))


@app.route('/api/trends')
def api_trends():
    stats = db.get_sensor_stats()
    if not stats:
        return jsonify({})

    def delta(curr_key, prev_key):
        c = stats.get(curr_key)
        p = stats.get(prev_key)
        if c is None or p is None:
            return None
        return round(c - p, 2)

    def stat_block(h1_mi, h1_av, h1_ma, h24_mi, h24_av, h24_ma, all_mi, all_ma):
        return {
            'h1_min':   stats.get(h1_mi),  'h1_avg':  stats.get(h1_av),  'h1_max':  stats.get(h1_ma),
            'h24_min':  stats.get(h24_mi), 'h24_avg': stats.get(h24_av), 'h24_max': stats.get(h24_ma),
            'all_min':  stats.get(all_mi), 'all_max': stats.get(all_ma),
        }

    return jsonify({
        'air_temp':   {'delta': delta('air_temp', 'prev_air_temp'),
                       **stat_block('h1_mi_t','h1_av_t','h1_ma_t','h24_mi_t','h24_av_t','h24_ma_t','all_mi_t','all_ma_t')},
        'air_hum':    {'delta': delta('air_hum', 'prev_air_hum'),
                       **stat_block('h1_mi_h','h1_av_h','h1_ma_h','h24_mi_h','h24_av_h','h24_ma_h','all_mi_h','all_ma_h')},
        'soil_temp':  {'delta': delta('soil_temp', 'prev_soil_temp'),
                       **stat_block('h1_mi_st','h1_av_st','h1_ma_st','h24_mi_st','h24_av_st','h24_ma_st','all_mi_st','all_ma_st')},
        'soil_moist': {'delta': delta('soil_moist', 'prev_soil_moist'),
                       **stat_block('h1_mi_sm','h1_av_sm','h1_ma_sm','h24_mi_sm','h24_av_sm','h24_ma_sm','all_mi_sm','all_ma_sm')},
        'pressure':   {'delta': delta('pressure', 'prev_pressure'),
                       **stat_block('h1_mi_p','h1_av_p','h1_ma_p','h24_mi_p','h24_av_p','h24_ma_p','all_mi_p','all_ma_p')},
        'mq7':        {**stat_block('h1_mi_mq7','h1_av_mq7','h1_ma_mq7','h24_mi_mq7','h24_av_mq7','h24_ma_mq7','all_mi_mq7','all_ma_mq7')},
        'mq135':      {**stat_block('h1_mi_mq135','h1_av_mq135','h1_ma_mq135','h24_mi_mq135','h24_av_mq135','h24_ma_mq135','all_mi_mq135','all_ma_mq135')},
        'total_rows': stats.get('all_total_rows', 0),
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


@app.route('/api/camera/history')
def api_camera_history():
    from flask import request as req
    hours = req.args.get('hours', 24, type=int)
    hours = min(max(hours, 1), 720)
    return jsonify(db.get_sky_history(hours))


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
