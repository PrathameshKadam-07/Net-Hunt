import json
import pandas as pd
import pickle
import os
from sklearn.ensemble import IsolationForest

LOG_FILE = "honeypot_logs.json"
MODEL_FILE = "model.pkl"


# ---------------- TRAIN MODEL ---------------- #
def train_model(df):
    ip_counts = df['ip'].value_counts().to_dict()
    df['ip_freq'] = df['ip'].map(ip_counts)

    service_counts = df['service'].value_counts().to_dict()
    df['service_freq'] = df['service'].map(service_counts)

    df['is_failed'] = df['status'].apply(
        lambda x: 1 if 'fail' in str(x).lower() else 0
    )

    features = df[['ip_freq', 'service_freq', 'is_failed']]

    model = IsolationForest(contamination=0.2)
    model.fit(features)

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

    return model


# ---------------- LOAD MODEL ---------------- #
def load_model():
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, "rb") as f:
            return pickle.load(f)
    return None


# ---------------- DETECT ANOMALIES ---------------- #
def detect_anomalies():
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        return []

    if not logs:
        return []

    df = pd.DataFrame(logs)

    # Feature Engineering
    ip_counts = df['ip'].value_counts().to_dict()
    df['ip_freq'] = df['ip'].map(ip_counts)

    service_counts = df['service'].value_counts().to_dict()
    df['service_freq'] = df['service'].map(service_counts)

    df['is_failed'] = df['status'].apply(
        lambda x: 1 if 'fail' in str(x).lower() else 0
    )

    features = df[['ip_freq', 'service_freq', 'is_failed']]

    # Load or train model
    model = load_model()

    if model is None:
        print("⚠️ Training model...")
        model = train_model(df)

    # Predict
    df['anomaly'] = model.predict(features)

    df['ai_flag'] = df['anomaly'].apply(
        lambda x: "🚨 Anomaly" if x == -1 else "Normal"
    )

    return df.to_dict(orient="records")
