import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import json
import joblib
import pandas as pd
import streamlit as st

from src.predict import load_artifacts, score_to_risk_band

st.set_page_config(
    page_title="AMEX Credit Risk Dashboard",
    page_icon="📉",
    layout="wide"
)

st.title("AMEX Credit Risk Early Warning System")

model, feature_columns, metrics, threshold_df, importance_df = load_artifacts()

st.subheader("Model Summary")
st.write(metrics)

st.subheader("Single Customer Risk Prediction")

default_values = {}
for col in feature_columns:
    default_values[col] = -999.0

with st.form("prediction_form"):
    user_inputs = {}
    preview_features = feature_columns[:12]

    for col in preview_features:
        user_inputs[col] = st.number_input(col, value=float(default_values[col]))

    submitted = st.form_submit_button("Predict Risk")

if submitted:
    X_input = pd.DataFrame([{col: user_inputs.get(col, -999.0) for col in feature_columns}])
    risk_score = float(model.predict_proba(X_input)[:, 1][0])
    risk_band = score_to_risk_band(risk_score)
    predicted_class = int(risk_score >= 0.5)

    st.metric("Risk Score", f"{risk_score:.4f}")
    st.metric("Predicted Class", predicted_class)
    st.metric("Risk Band", risk_band)

if importance_df is not None:
    st.subheader("Top Feature Importances")
    st.dataframe(importance_df.head(20), use_container_width=True)

if threshold_df is not None:
    st.subheader("Threshold Metrics")
    st.dataframe(threshold_df, use_container_width=True)
