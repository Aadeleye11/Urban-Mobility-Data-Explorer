import sqlite3
from flask_cors import CORS
from flask import Flask, jsonify, request
from db_setup import setup_and_import  # Make sure db_setup.py is in the same folder

# Ensure the database and indexes are set up before starting the API
setup_and_import()

DB_FILENAME = 'train.db'

def get_db_conn():
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
CORS(app)
# KPI Indicators
@app.route('/api/kpi')
def api_kpi():
    vendor = request.args.get('vendor')
    start = request.args.get('start')
    end = request.args.get('end')
    conn = get_db_conn()
    cursor = conn.cursor()
    sql = "SELECT COUNT(*), AVG(distance_km), AVG(trip_duration), AVG(passenger_count) FROM train_trips WHERE 1=1"
    params = []
    if vendor:
        sql += " AND vendor_id=?"
        params.append(vendor)
    if start:
        sql += " AND DATE(pickup_datetime) >= ?"
        params.append(start)
    if end:
        sql += " AND DATE(pickup_datetime) <= ?"
        params.append(end)
    cursor.execute(sql, params)
    row = cursor.fetchone()
    conn.close()
    return jsonify({
        "total_trips": row[0],
        "avg_distance": row[1],
        "avg_duration": row[2],
        "avg_passengers": row[3]
    })
# TRIP COUNT BY DAY AND PASSENGER COUNT (LINE CHART)
@app.route('/api/trips_by_day')
def api_trips_by_day():
    start = request.args.get('start')
    end = request.args.get('end')
    conn = get_db_conn()
    cursor = conn.cursor()
    sql = """
        SELECT DATE(pickup_datetime) AS day,
               COUNT(*) AS trip_count,
               SUM(passenger_count) AS passenger_count
        FROM train_trips
        WHERE 1=1
    """
    params = []
    if start:
        sql += " AND DATE(pickup_datetime) >= ?"
        params.append(start)
    if end:
        sql += " AND DATE(pickup_datetime) <= ?"
        params.append(end)
    sql += " GROUP BY day ORDER BY day"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return jsonify(data)

# AVG SPEED BY HOUR (BAR CHART BY VENDOR)
@app.route('/api/avg_speed_by_hour_by_vendor')
def api_avg_speed_by_hour_by_vendor():
    start = request.args.get('start')
    end = request.args.get('end')
    conn = get_db_conn()
    cursor = conn.cursor()
    sql = """
        SELECT strftime('%H', pickup_datetime) AS hour,
               vendor_id,
               AVG(speed_km_min * 60) AS avg_km_h
        FROM train_trips
        WHERE 1=1
    """
    params = []
    if start:
        sql += " AND DATE(pickup_datetime) >= ?"
        params.append(start)
    if end:
        sql += " AND DATE(pickup_datetime) <= ?"
        params.append(end)
    sql += " GROUP BY hour, vendor_id ORDER BY hour, vendor_id"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return jsonify(data)

# TRIPS PER HOUR (BAR CHART BY VENDOR)
@app.route('/api/trips_per_hour_by_vendor')
def api_trips_per_hour_by_vendor():
    start = request.args.get('start')
    end = request.args.get('end')
    conn = get_db_conn()
    cursor = conn.cursor()
    sql = """
        SELECT strftime('%H', pickup_datetime) AS hour,
               vendor_id,
               COUNT(*) AS trip_count
        FROM train_trips
        WHERE 1=1
    """
    params = []
    if start:
        sql += " AND DATE(pickup_datetime) >= ?"
        params.append(start)
    if end:
        sql += " AND DATE(pickup_datetime) <= ?"
        params.append(end)
    sql += " GROUP BY hour, vendor_id ORDER BY hour, vendor_id"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return jsonify(data)

# TRIPS BY VENDOR (PIE CHART)
@app.route('/api/trips_by_vendor')
def api_trips_by_vendor():
    start = request.args.get('start')
    end = request.args.get('end')
    conn = get_db_conn()
    cursor = conn.cursor()
    sql = """
        SELECT vendor_id, COUNT(*) AS trip_count
        FROM train_trips
        WHERE 1=1
    """
    params = []
    if start:
        sql += " AND DATE(pickup_datetime) >= ?"
        params.append(start)
    if end:
        sql += " AND DATE(pickup_datetime) <= ?"
        params.append(end)
    sql += " GROUP BY vendor_id"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
