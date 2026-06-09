from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = '/home/pawan/iesh_data.db'

def get_db_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # Grab the 50 most recent logs
        c.execute("SELECT * FROM sensor_logs ORDER BY timestamp DESC LIMIT 50")
        rows = c.fetchall()
        conn.close()
        # Reverse the list so the oldest is first (better for graphs)
        return [dict(row) for row in rows][::-1]
    except Exception as e:
        print(f"DB Error: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def data():
    history = get_db_data()
    latest = history[-1] if history else None
    return jsonify({'latest': latest, 'history': history})

if __name__ == '__main__':
    # host='0.0.0.0' allows devices on the Wi-Fi hotspot to see the server
    app.run(host='0.0.0.0', port=5000, debug=True)
