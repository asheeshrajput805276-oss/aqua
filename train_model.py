from pathlib import Path
import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# ==========================================
# LOAD DATASET
# ==========================================

data = pd.read_csv("data/sensor_data.csv")

print("✅ Dataset loaded")
print("Total records:", len(data))

# ==========================================
# SELECT SENSOR FEATURES
# ==========================================

features = [
    "flow_lpm",
    "pressure_bar",
    "moisture_pct",
    "water_level_m"
]

X = data[features]

# ==========================================
# TRAIN AI MODEL
# ==========================================

model = Pipeline([
    ("scaler", StandardScaler()),
    (
        "isolation_forest",
        IsolationForest(
            n_estimators=150,
            contamination=0.08,
            random_state=42
        )
    )
])

model.fit(X)

# ==========================================
# SAVE MODEL
# ==========================================

Path("model").mkdir(exist_ok=True)
joblib.dump(model, "model/ai_anomaly_model.pkl")

print("✅ AI model trained using CSV dataset!")
print("✅ Model saved as model/ai_anomaly_model.pkl")