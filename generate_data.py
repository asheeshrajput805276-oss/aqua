import csv
import random
from datetime import datetime, timedelta

random.seed(42)

rows = []

start_time = datetime.now() - timedelta(hours=8)

# -----------------------------------------
# 1. NORMAL DATA
# -----------------------------------------

for i in range(400):

    timestamp = start_time + timedelta(minutes=i)

    flow = random.uniform(78, 85)
    pressure = random.uniform(3.4, 3.9)
    moisture = random.uniform(40, 48)
    water_level = random.uniform(3.5, 4.0)

    zone = random.choice(["A1", "A2", "B1", "B2"])
    status = "NORMAL"

    rows.append([
        timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        zone,
        round(flow, 2),
        round(pressure, 2),
        round(moisture, 2),
        round(water_level, 2),
        status
    ])


# -----------------------------------------
# 2. WARNING DATA
# -----------------------------------------

for i in range(60):

    timestamp = start_time + timedelta(minutes=400 + i)

    flow = random.uniform(68, 77)
    pressure = random.uniform(2.8, 3.3)
    moisture = random.uniform(50, 60)
    water_level = random.uniform(3.2, 3.5)

    zone = random.choice(["B1", "B2"])
    status = "WARNING"

    rows.append([
        timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        zone,
        round(flow, 2),
        round(pressure, 2),
        round(moisture, 2),
        round(water_level, 2),
        status
    ])


# -----------------------------------------
# 3. LEAK DATA — B2
# -----------------------------------------

for i in range(40):

    timestamp = start_time + timedelta(minutes=460 + i)

    flow = random.uniform(55, 65)
    pressure = random.uniform(2.0, 2.6)
    moisture = random.uniform(62, 72)
    water_level = random.uniform(3.0, 3.5)

    zone = "B2"
    status = "LEAK"

    rows.append([
        timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        zone,
        round(flow, 2),
        round(pressure, 2),
        round(moisture, 2),
        round(water_level, 2),
        status
    ])


# -----------------------------------------
# SAVE CSV
# -----------------------------------------

file_path = "data/sensor_data.csv"

with open(file_path, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "timestamp",
        "zone",
        "flow_lpm",
        "pressure_bar",
        "moisture_pct",
        "water_level_m",
        "status"
    ])

    writer.writerows(rows)

print("✅ Dataset generated successfully!")
print(f"✅ Total records: {len(rows)}")
print(f"✅ Saved to: {file_path}")