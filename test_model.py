import numpy as np
import joblib

# ==========================================
# LOAD TRAINED AI MODEL
# ==========================================

model = joblib.load("ai_anomaly_model.pkl")

print("\n🤖 AquaTech AI Model Test")
print("=" * 40)


# ==========================================
# FUNCTION FOR TESTING
# ==========================================

def test_condition(name, flow, pressure, moisture, water_level):

    sensor_data = np.array([[
        flow,
        pressure,
        moisture,
        water_level
    ]])

    prediction = model.predict(sensor_data)[0]

    if prediction == -1:
        result = "🔴 ANOMALY DETECTED"
    else:
        result = "🟢 NORMAL"

    print(f"\n{name}")
    print(f"Flow: {flow} L/min")
    print(f"Pressure: {pressure} bar")
    print(f"Moisture: {moisture}%")
    print(f"Water Level: {water_level} m")
    print(f"AI Result: {result}")


# ==========================================
# TEST 1 — NORMAL
# ==========================================

test_condition(
    "TEST 1 — NORMAL CONDITION",
    82,
    3.7,
    45,
    3.8
)


# ==========================================
# TEST 2 — WARNING
# ==========================================

test_condition(
    "TEST 2 — WARNING CONDITION",
    72,
    3.1,
    55,
    3.4
)


# ==========================================
# TEST 3 — B2 LEAK
# ==========================================

test_condition(
    "TEST 3 — B2 LEAK CONDITION",
    60,
    2.3,
    68,
    3.2
)


print("\n" + "=" * 40)
print("✅ AI testing completed!")