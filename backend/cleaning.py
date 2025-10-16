"""
Train Data Cleaning and Speed Calculation Script
- Cleans malformed latitude values (removes apostrophes)
- Drops records with passenger_count == 0
- Converts trip_duration from seconds to minutes
- Calculates trip distance with Haversine formula
- Calculates speed in km/min (distance divided by minutes)
- Saves cleaned and excluded records to CSV
"""

import csv
from math import radians, sin, cos, sqrt, atan2

# Helper functions
def clean_latitude(value):
    unwanted = "'"
    try:
        if unwanted in value:
            value = value.replace(unwanted, "")
        return float(value)
    except:
        return None

def convert_duration_to_minutes(value):
    try:
        return float(value) / 60  # Converts seconds to minutes
    except:
        return None

def haversine_distance(lat1, lon1, lat2, lon2):
    try:
        R = 6371.0  # Earth radius in km
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return round(R * c, 3)
    except:
        return None

# Load raw CSV file
filename = r"C:\Users\asade\Downloads\SUMMATIVE\train.csv"
data = []
with open(filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

cleaned_data = []
excluded_records = []

for row in data:
    # Clean latitude fields
    row['pickup_latitude'] = clean_latitude(row['pickup_latitude'])
    row['dropoff_latitude'] = clean_latitude(row['dropoff_latitude'])

    # Convert longitude fields
    try:
        row['pickup_longitude'] = float(row['pickup_longitude'])
        row['dropoff_longitude'] = float(row['dropoff_longitude'])
    except:
        excluded_records.append(row)
        continue

    # Exclude if latitude or longitude conversion failed
    if None in (row['pickup_latitude'], row['dropoff_latitude'], row['pickup_longitude'], row['dropoff_longitude']):
        excluded_records.append(row)
        continue

    # Convert trip_duration from seconds to minutes
    row['trip_duration_min'] = convert_duration_to_minutes(row['trip_duration'])
    if row['trip_duration_min'] is None:
        excluded_records.append(row)
        continue

    # Exclude if passenger_count == 0
    try:
        if int(row['passenger_count']) == 0:
            excluded_records.append(row)
            continue
    except:
        excluded_records.append(row)
        continue

    # Calculate distance in km
    row['distance_km'] = haversine_distance(
        row['pickup_latitude'],
        row['pickup_longitude'],
        row['dropoff_latitude'],
        row['dropoff_longitude']
    )
    if row['distance_km'] is None or row['distance_km'] == 0:
        excluded_records.append(row)
        continue

    # Calculate speed (km per minute)
    try:
        if row['trip_duration_min'] > 0:
            row['speed_km_min'] = round(row['distance_km'] / row['trip_duration_min'], 4)
        else:
            row['speed_km_min'] = None
    except:
        row['speed_km_min'] = None

    cleaned_data.append(row)

print(f"Cleaning done: {len(cleaned_data)} records kept, {len(excluded_records)} excluded.")

# Save cleaned records
if cleaned_data:
    with open('train_cleaned.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cleaned_data[0].keys())
        writer.writeheader()
        writer.writerows(cleaned_data)

# Save excluded records for documentation
if excluded_records:
    with open('excluded_records.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=excluded_records[0].keys())
        writer.writeheader()
        writer.writerows(excluded_records)
