import streamlit as st
import pandas as pd
import joblib
import random
import time
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AquaTech AI",
    page_icon="💧",
    layout="wide"
)

# =====================================================
# LOAD AI MODEL
# =====================================================

MODEL_PATH = Path("model/ai_anomaly_model.pkl")
DATA_PATH = Path("data/sensor_data.csv")

try:
    model = joblib.load(MODEL_PATH)
    model_loaded = True
except Exception:
    model_loaded = False

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0b1220;
}

.block-container {
    padding-top: 1.5rem;
}

h1 {
    font-size: 38px !important;
}

.metric-card {
    background: #111827;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #263244;
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #94a3b8;
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
}

.panel {
    background: #111827;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #263244;
}

.live {
    color: #22c55e;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

header1, header2 = st.columns([4, 1])

with header1:
    st.title("💧 AquaTech")
    st.subheader(
        "AI-Powered Groundwater & Pipeline Leakage Monitoring System"
    )

with header2:
    st.markdown(
        '<h3 class="live">● LIVE</h3>',
        unsafe_allow_html=True
    )

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎛️ Demo Control")

simulate_leak = st.sidebar.checkbox(
    "🔴 Simulate Leak — B2"
)

st.sidebar.divider()

if model_loaded:
    st.sidebar.success("🤖 AI Model Connected")
else:
    st.sidebar.error("❌ AI Model Not Found")

# =====================================================
# SENSOR SIMULATION
# =====================================================

if simulate_leak:

    flow = random.uniform(56, 65)
    pressure = random.uniform(2.0, 2.6)
    moisture = random.uniform(62, 72)
    water_level = random.uniform(3.0, 3.5)
    current_zone = "B2"

else:

    flow = random.uniform(78, 85)
    pressure = random.uniform(3.4, 3.9)
    moisture = random.uniform(40, 48)
    water_level = random.uniform(3.5, 4.0)
    current_zone = "A1"

# =====================================================
# AI MODEL PREDICTION
# =====================================================

sensor_input = pd.DataFrame([{
    "flow_lpm": flow,
    "pressure_bar": pressure,
    "moisture_pct": moisture,
    "water_level_m": water_level
}])

if model_loaded:

    ai_prediction = model.predict(sensor_input)[0]

    if ai_prediction == -1:
        ai_status = "ANOMALY"
    else:
        ai_status = "NORMAL"

else:

    ai_prediction = 1
    ai_status = "MODEL ERROR"

# =====================================================
# LEAK RISK SCORE
# =====================================================

flow_risk = max(0, (82 - flow) / 27 * 100)

pressure_risk = max(
    0,
    (3.7 - pressure) / 1.7 * 100
)

moisture_risk = max(
    0,
    (moisture - 45) / 30 * 100
)

risk_score = (
    flow_risk * 0.35 +
    pressure_risk * 0.35 +
    moisture_risk * 0.30
)

# AI anomaly increases confidence
if ai_status == "ANOMALY":
    risk_score = max(risk_score, 75)

risk_score = min(risk_score, 99)

# =====================================================
# STATUS
# =====================================================

if risk_score >= 75:

    risk_status = "HIGH"
    zone_status = "🔴 B2"

elif risk_score >= 40:

    risk_status = "MEDIUM"
    zone_status = "🟡 B2"

else:

    risk_status = "LOW"
    zone_status = "🟢 NORMAL"

# =====================================================
# ALERT
# =====================================================

if ai_status == "ANOMALY" and risk_score >= 75:

    st.error(
        "🚨 LEAK DETECTED — AI MODEL IDENTIFIED ABNORMAL PIPELINE BEHAVIOUR"
    )

elif ai_status == "ANOMALY":

    st.warning(
        "⚠️ AI ANOMALY DETECTED — VERIFICATION REQUIRED"
    )

else:

    st.success(
        "🟢 SYSTEM NORMAL — AI FOUND NO MAJOR ANOMALY"
    )

# =====================================================
# SENSOR CARDS
# =====================================================

st.markdown("### 📡 Live Sensor Data")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "💧 Flow",
        f"{flow:.1f} L/min"
    )

with c2:
    st.metric(
        "⚙️ Pressure",
        f"{pressure:.2f} bar"
    )

with c3:
    st.metric(
        "🌱 Moisture",
        f"{moisture:.1f}%"
    )

with c4:
    st.metric(
        "🌊 Water Level",
        f"{water_level:.2f} m"
    )

with c5:
    st.metric(
        "🚨 Leak Risk",
        f"{risk_score:.0f}%"
    )

# =====================================================
# PIPELINE MAP + AI PANEL
# =====================================================

st.markdown("---")

map_col, ai_col = st.columns([2, 1])

# =====================================================
# PIPELINE MAP
# =====================================================

with map_col:

    st.markdown("### 🗺️ Live Pipeline Map")

    if simulate_leak:

        st.markdown("""
        <div class="panel">

        💧 <b>SOURCE</b>

        ↓

        🟢 <b>A1</b>
        ━━━━━
        🟢 <b>A2</b>
        ━━━━━
        🟢 <b>B1</b>
        ━━━━━
        <span style="color:red;font-size:24px;">
        🔴 <b>B2</b>
        </span>

        <br><br>

        ⚠️ <b>PROBABLE LEAKAGE ZONE</b>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="panel">

        💧 <b>SOURCE</b>

        ↓

        🟢 <b>A1</b>
        ━━━━━
        🟢 <b>A2</b>
        ━━━━━
        🟢 <b>B1</b>
        ━━━━━
        🟢 <b>B2</b>

        <br><br>

        🟢 <b>PIPELINE STATUS: NORMAL</b>

        </div>
        """, unsafe_allow_html=True)

# =====================================================
# AI PANEL
# =====================================================

with ai_col:

    st.markdown("### 🤖 AI Analysis")

    if ai_status == "ANOMALY":

        st.error("🔴 ANOMALY DETECTED")

        st.write(
            "**Probable Zone:** B2"
        )

        st.write(
            f"**Risk Level:** {risk_status}"
        )

        st.write(
            f"**Risk Score:** {risk_score:.0f}%"
        )

        st.write(
            "AI observed abnormal sensor behaviour."
        )

        st.write(
            "Flow ↓ + Pressure ↓ + Moisture ↑"
        )

    else:

        st.success("🟢 NORMAL BEHAVIOUR")

        st.write(
            "**AI Status:** Normal"
        )

        st.write(
            f"**Risk Score:** {risk_score:.0f}%"
        )

        st.write(
            "Sensor pattern is within normal range."
        )

# =====================================================
# ZONE STATUS
# =====================================================

st.markdown("---")

st.markdown("### 📍 Zone Status")

z1, z2, z3, z4 = st.columns(4)

with z1:
    st.info("🟢 A1\n\nNormal")

with z2:
    st.info("🟢 A2\n\nNormal")

with z3:
    st.info("🟢 B1\n\nNormal")

with z4:

    if simulate_leak:
        st.error("🔴 B2\n\nLEAK")
    else:
        st.info("🟢 B2\n\nNormal")

# =====================================================
# LIVE GRAPH DATA
# =====================================================

if "flow_history" not in st.session_state:
    st.session_state.flow_history = []

if "pressure_history" not in st.session_state:
    st.session_state.pressure_history = []

if "moisture_history" not in st.session_state:
    st.session_state.moisture_history = []

# Store latest values
st.session_state.flow_history.append(flow)
st.session_state.pressure_history.append(pressure)
st.session_state.moisture_history.append(moisture)

# Keep last 30 values
st.session_state.flow_history = \
    st.session_state.flow_history[-30:]

st.session_state.pressure_history = \
    st.session_state.pressure_history[-30:]

st.session_state.moisture_history = \
    st.session_state.moisture_history[-30:]

# =====================================================
# GRAPHS
# =====================================================

st.markdown("---")

g1, g2, g3 = st.columns(3)

with g1:

    st.markdown("### 💧 Flow")

    st.line_chart(
        st.session_state.flow_history
    )

with g2:

    st.markdown("### ⚙️ Pressure")

    st.line_chart(
        st.session_state.pressure_history
    )

with g3:

    st.markdown("### 🌱 Moisture")

    st.line_chart(
        st.session_state.moisture_history
    )

# =====================================================
# AI MODEL INFORMATION
# =====================================================

st.markdown("---")

st.markdown("### 🧠 AI Model")

if model_loaded:

    st.success(
        "Isolation Forest AI model connected successfully"
    )

    st.write(
        "The model analyses Flow, Pressure, Moisture "
        "and Water Level to identify abnormal behaviour."
    )

else:

    st.error(
        "AI model file could not be loaded."
    )
    # =====================================================
# DATASET & AI PERFORMANCE
# =====================================================

st.markdown("---")

st.markdown("### 📊 AI Model Performance")

try:

    dataset = pd.read_csv(DATA_PATH)

    total_records = len(dataset)

    normal_records = (
        dataset["status"] == "NORMAL"
    ).sum()

    warning_records = (
        dataset["status"] == "WARNING"
    ).sum()

    leak_records = (
        dataset["status"] == "LEAK"
    ).sum()

    # AI prediction on complete dataset
    dataset_features = dataset[
        [
            "flow_lpm",
            "pressure_bar",
            "moisture_pct",
            "water_level_m"
        ]
    ]

    dataset_prediction = model.predict(
        dataset_features
    )

    dataset["ai_prediction"] = dataset_prediction

    # Check actual leak records
    actual_leaks = dataset[
        dataset["status"] == "LEAK"
    ]

    detected_leaks = (
        actual_leaks["ai_prediction"] == -1
    ).sum()

    if leak_records > 0:
        detection_rate = (
            detected_leaks / leak_records
        ) * 100
    else:
        detection_rate = 0

    # -------------------------------
    # METRICS
    # -------------------------------

    p1, p2, p3, p4, p5 = st.columns(5)

    with p1:
        st.metric(
            "📁 Total Records",
            total_records
        )

    with p2:
        st.metric(
            "🟢 Normal",
            normal_records
        )

    with p3:
        st.metric(
            "🟡 Warning",
            warning_records
        )

    with p4:
        st.metric(
            "🔴 Leak",
            leak_records
        )

    with p5:
        st.metric(
            "🤖 Detection Rate",
            f"{detection_rate:.1f}%"
        )

    # -------------------------------
    # AI RESULT
    # -------------------------------

    st.markdown("#### 🤖 AI Evaluation")

    if detection_rate >= 90:

        st.success(
            f"✅ AI detected {detected_leaks} "
            f"out of {leak_records} actual leak records."
        )

    else:

        st.warning(
            f"⚠️ AI detected {detected_leaks} "
            f"out of {leak_records} actual leak records."
        )

    st.info(
        "The AI model uses Flow, Pressure, Moisture "
        "and Water Level to identify abnormal pipeline behaviour."
    )

except Exception as e:

    st.error(
        f"Dataset analysis error: {e}"
    )
    # =====================================================
# CSV LIVE DATA + AI PREDICTION
# =====================================================
# =====================================================
# AI DECISION ENGINE + MULTI-SENSOR VERIFICATION
# =====================================================

st.markdown("---")
st.markdown("### 🔍 Multi-Sensor Verification")

# ---------------------------------------------
# SENSOR CONDITION CHECK
# ---------------------------------------------

flow_abnormal = flow < 70
pressure_abnormal = pressure < 3.0
moisture_abnormal = moisture > 55
water_level_abnormal = water_level < 3.4

# ---------------------------------------------
# COUNT ABNORMAL SENSORS
# ---------------------------------------------

abnormal_count = sum([
    flow_abnormal,
    pressure_abnormal,
    moisture_abnormal,
    water_level_abnormal
])

# ---------------------------------------------
# SENSOR STATUS
# ---------------------------------------------

v1, v2, v3, v4 = st.columns(4)

with v1:
    if flow_abnormal:
        st.error("🔴 FLOW\n\nABNORMAL")
    else:
        st.success("🟢 FLOW\n\nNORMAL")

with v2:
    if pressure_abnormal:
        st.error("🔴 PRESSURE\n\nABNORMAL")
    else:
        st.success("🟢 PRESSURE\n\nNORMAL")

with v3:
    if moisture_abnormal:
        st.error("🔴 MOISTURE\n\nABNORMAL")
    else:
        st.success("🟢 MOISTURE\n\nNORMAL")

with v4:
    if water_level_abnormal:
        st.warning("🟡 WATER LEVEL\n\nWARNING")
    else:
        st.success("🟢 WATER LEVEL\n\nNORMAL")

# ---------------------------------------------
# DECISION ENGINE
# ---------------------------------------------

if ai_status == "ANOMALY" and abnormal_count >= 3:

    verification_status = "VERIFIED"
    decision = "LEAK DETECTED"
    decision_icon = "🔴"

elif ai_status == "ANOMALY" and abnormal_count >= 2:

    verification_status = "REVIEW REQUIRED"
    decision = "POSSIBLE LEAK"
    decision_icon = "🟡"

elif abnormal_count >= 2:

    verification_status = "REVIEW REQUIRED"
    decision = "ABNORMAL PATTERN"
    decision_icon = "🟡"

else:

    verification_status = "NORMAL"
    decision = "NO LEAK DETECTED"
    decision_icon = "🟢"

# ---------------------------------------------
# VERIFICATION RESULT
# ---------------------------------------------

st.markdown("#### 🤖 Decision Engine Result")

r1, r2, r3 = st.columns(3)

with r1:
    st.metric(
        "Abnormal Sensors",
        f"{abnormal_count}/4"
    )

with r2:
    st.metric(
        "AI Prediction",
        ai_status
    )

with r3:
    st.metric(
        "Verification",
        verification_status
    )

if verification_status == "VERIFIED":

    st.error(
        f"{decision_icon} **{decision} — B2**"
    )

    st.write(
        "Multiple sensor parameters and the AI anomaly "
        "prediction indicate a high-risk leakage pattern."
    )

elif verification_status == "REVIEW REQUIRED":

    st.warning(
        f"{decision_icon} **{decision}**"
    )

    st.write(
        "Abnormal sensor behaviour detected. "
        "Further verification is recommended."
    )

else:

    st.success(
        f"{decision_icon} **{decision}**"
    )

    st.write(
        "Sensor parameters are currently within "
        "the expected operating range."
    )

# ---------------------------------------------
# DETECTION REASON
# ---------------------------------------------

st.markdown("#### 🧠 Detection Reason")

reasons = []

if flow_abnormal:
    reasons.append("Flow ↓")

if pressure_abnormal:
    reasons.append("Pressure ↓")

if moisture_abnormal:
    reasons.append("Moisture ↑")

if water_level_abnormal:
    reasons.append("Water Level ↓")

if reasons:

    st.info(
        " + ".join(reasons)
    )

else:

    st.info(
        "All monitored parameters are within normal range."
    )
st.markdown("---")
st.markdown("### 📋 Live Sensor Records")

try:

    csv_data = pd.read_csv(DATA_PATH)

    # Select latest 10 records
    latest_data = csv_data.tail(10).copy()

    # AI prediction
    latest_features = latest_data[
        [
            "flow_lpm",
            "pressure_bar",
            "moisture_pct",
            "water_level_m"
        ]
    ]

    latest_prediction = model.predict(
        latest_features
    )

    latest_data["AI Prediction"] = [
        "🔴 ANOMALY" if x == -1 else "🟢 NORMAL"
        for x in latest_prediction
    ]

    # Display table
    st.dataframe(
        latest_data[
            [
                "timestamp",
                "zone",
                "flow_lpm",
                "pressure_bar",
                "moisture_pct",
                "water_level_m",
                "status",
                "AI Prediction"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

except Exception as e:

    st.error(
        f"CSV data error: {e}"
    )


# =====================================================
# ZONE-WISE AI ANALYSIS
# =====================================================

st.markdown("---")
st.markdown("### 📍 Zone-Wise AI Analysis")

try:

    zone_data = pd.read_csv(DATA_PATH)

    zone_features = zone_data[
        [
            "flow_lpm",
            "pressure_bar",
            "moisture_pct",
            "water_level_m"
        ]
    ]

    zone_prediction = model.predict(
        zone_features
    )

    zone_data["ai_anomaly"] = (
        zone_prediction == -1
    )

    # Count AI anomalies by zone
    zone_anomalies = (
        zone_data
        .groupby("zone")["ai_anomaly"]
        .sum()
        .reset_index()
    )

    zone_anomalies.columns = [
        "Zone",
        "AI Anomalies"
    ]

    st.bar_chart(
        zone_anomalies.set_index("Zone")
    )

    # Most suspicious zone
    highest_zone = zone_anomalies.loc[
        zone_anomalies["AI Anomalies"].idxmax()
    ]

    st.info(
        f"🤖 AI Analysis: **{highest_zone['Zone']}** "
        f"has the highest number of abnormal readings "
        f"({int(highest_zone['AI Anomalies'])})."
    )

except Exception as e:

    st.error(
        f"Zone analysis error: {e}"
    )

# =====================================================
# AUTO REFRESH
# =====================================================

time.sleep(2)
st.rerun()