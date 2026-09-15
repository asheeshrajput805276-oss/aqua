import pandas as pd
import joblib

# ==========================================
# LOAD DATASET
# ==========================================

data = pd.read_csv("data/sensor_data.csv")

print("==========================================")
print("        AquaTech AI Model Evaluation")
print("==========================================")

print("\n✅ Dataset loaded")
print("Total records:", len(data))

# ==========================================
# LOAD TRAINED AI MODEL
# ==========================================

model = joblib.load("model/ai_anomaly_model.pkl")

print("✅ AI model loaded successfully")

# ==========================================
# SENSOR FEATURES
# ==========================================

features = [
    "flow_lpm",
    "pressure_bar",
    "moisture_pct",
    "water_level_m"
]

X = data[features]

# ==========================================
# AI PREDICTION
# ==========================================

# Isolation Forest:
#  1  = Normal
# -1  = Anomaly

prediction = model.predict(X)

data["ai_prediction"] = prediction

# Convert Isolation Forest output
data["ai_status"] = data["ai_prediction"].apply(
    lambda x: "ANOMALY" if x == -1 else "NORMAL"
)

# ==========================================
# RESULTS
# ==========================================

total = len(data)

normal_ai = (data["ai_status"] == "NORMAL").sum()
anomaly_ai = (data["ai_status"] == "ANOMALY").sum()

actual_normal = (data["status"] == "NORMAL").sum()
actual_warning = (data["status"] == "WARNING").sum()
actual_leak = (data["status"] == "LEAK").sum()

print("\n------------------------------------------")
print("ACTUAL DATASET STATUS")
print("------------------------------------------")

print("NORMAL records :", actual_normal)
print("WARNING records:", actual_warning)
print("LEAK records   :", actual_leak)

print("\n------------------------------------------")
print("AI MODEL PREDICTION")
print("------------------------------------------")

print("Normal detected :", normal_ai)
print("Anomaly detected:", anomaly_ai)

print("\n------------------------------------------")
print("LEAK DETECTION CHECK")
print("------------------------------------------")

# Check actual LEAK rows
leak_rows = data[data["status"] == "LEAK"]

leak_detected = (
    leak_rows["ai_status"] == "ANOMALY"
).sum()

leak_total = len(leak_rows)

if leak_total > 0:
    leak_detection_rate = (
        leak_detected / leak_total
    ) * 100

    print("Actual LEAK records :", leak_total)
    print("AI detected LEAKs   :", leak_detected)
    print(
        f"Leak Detection Rate : {leak_detection_rate:.2f}%"
    )
else:
    print("No LEAK records found.")

# ==========================================
# ZONE ANALYSIS
# ==========================================

print("\n------------------------------------------")
print("ZONE-WISE ANALYSIS")
print("------------------------------------------")

zones = data["zone"].unique()

for zone in zones:

    zone_data = data[data["zone"] == zone]

    actual_leaks = (
        zone_data["status"] == "LEAK"
    ).sum()

    ai_anomalies = (
        zone_data["ai_status"] == "ANOMALY"
    ).sum()

    print(
        f"{zone} -> Actual LEAK: {actual_leaks}, "
        f"AI Anomalies: {ai_anomalies}"
    )

# ==========================================
# SHOW LAST LEAK RECORDS
# ==========================================

print("\n------------------------------------------")
print("RECENT LEAK DATA")
print("------------------------------------------")

recent_leaks = data[
    data["status"] == "LEAK"
].tail(5)

if len(recent_leaks) > 0:

    print(
        recent_leaks[
            [
                "timestamp",
                "zone",
                "flow_lpm",
                "pressure_bar",
                "moisture_pct",
                "water_level_m",
                "status",
                "ai_status"
            ]
        ].to_string(index=False)
    )

else:
    print("No leak data available.")

# ==========================================
# FINAL RESULT
# ==========================================

print("\n==========================================")
print("          EVALUATION COMPLETE")
print("==========================================")

print("\nAquaTech AI successfully analyzed the")
print("pipeline sensor dataset.")

print("\nThe model uses:")
print("• Flow")
print("• Pressure")
print("• Moisture")
print("• Water Level")

print("\n==========================================")