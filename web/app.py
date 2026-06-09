"""HICS web dashboard — Flask app serving live telemetry from SQLite."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify
import data.database as db

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    history = db.get_recent(100)
    latest  = db.get_latest()
    return jsonify({'latest': latest, 'history': history})

@app.route('/api/latest')
def api_latest():
    return jsonify(db.get_latest() or {})

if __name__ == '__main__':
    db.init()
    # host='0.0.0.0' makes it reachable on both hotspot and ethernet
    app.run(host='0.0.0.0', port=5000, debug=False)
