import sqlite3
import csv
from datetime import datetime

DB_FILENAME = 'train.db'

def setup_and_import():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS train_trips (
        id TEXT PRIMARY KEY NOT NULL,
        vendor_id INTEGER NOT NULL,
        pickup_datetime TEXT NOT NULL,
        dropoff_datetime TEXT NOT NULL,
        passenger_count INTEGER NOT NULL,
        pickup_longitude REAL NOT NULL,
        pickup_latitude REAL NOT NULL,
        dropoff_longitude REAL NOT NULL,
        dropoff_latitude REAL NOT NULL,
        store_and_fwd_flag TEXT NOT NULL,
        trip_duration REAL NOT NULL,
        distance_km REAL NOT NULL,
        speed_km_min REAL NOT NULL
    );
    """)
    conn.commit()

    # Only import if table is empty
    cursor.execute("SELECT COUNT(*) FROM train_trips")
    if cursor.fetchone()[0] == 0:
        def parse_datetime(dt_str):
            return datetime.strptime(dt_str.strip(), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        with open("train_cleaned.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute("""
                    INSERT INTO train_trips (
                        id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count,
                        pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude,
                        store_and_fwd_flag, trip_duration, distance_km, speed_km_min
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['id'],
                    int(row['vendor_id']),
                    parse_datetime(row['pickup_datetime']),
                    parse_datetime(row['dropoff_datetime']),
                    int(row['passenger_count']),
                    float(row['pickup_longitude']),
                    float(row['pickup_latitude']),
                    float(row['dropoff_longitude']),
                    float(row['dropoff_latitude']),
                    row['store_and_fwd_flag'].strip(),
                    float(row['trip_duration']),
                    float(row['distance_km']),
                    float(row['speed_km_min'])
                ))
        conn.commit()

    # Create indexes for analytics
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pickup_datetime ON train_trips(pickup_datetime);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dropoff_datetime ON train_trips(dropoff_datetime);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_passenger_count ON train_trips(passenger_count);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendor_id ON train_trips(vendor_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_distance_km ON train_trips(distance_km);")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_and_import()
