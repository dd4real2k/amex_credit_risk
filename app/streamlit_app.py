import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.predict import load_artifacts, score_to_risk_band

st.set_page_config(
    page_title="AMEX Credit Risk Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Load artifacts
# -----------------------------
model, feature_columns, metrics, threshold_df, importance_df = load_artifacts()

# -----------------------------
# Helpers
# -----------------------------
def safe_metric(metrics_dict, model_key, metric_key, default=0.0):
    try:
        return metrics_dict.get(model_key, {}).get(metric_key, default)
    except Exception:
        return default

def build_input_dataframe(user_inputs: dict, feature_columns: list[str]) -> pd.DataFrame:
    row = {}
    for col in feature_columns:
        val = user_inputs.get(col, None)
        if val in ("", None):
            row[col] = -999
        else:
            row[col] = val
    return pd.DataFrame([row])

def predict_score(user_inputs: dict) -> tuple[float, int, str]:
    X_input = build_input_dataframe(user_inputs, feature_columns)
    risk_score = float(model.predict_proba(X_input)[:, 1][0])
    predicted_class = int(risk_score >= 0.5)
    risk_band = score_to_risk_band(risk_score)
    return risk_score, predicted_class, risk_band

def risk_band_color(risk_band: str) -> str:
    return {
        "Low": "#0f766e",
        "Medium": "#b45309",
        "High": "#b91c1c",
        "Critical": "#7f1d1d",
    }.get(risk_band, "#334155")

def recommendation_from_band(risk_band: str) -> str:
    if risk_band == "Low":
        return "Continue routine monitoring."
    if risk_band == "Medium":
        return "Monitor account closely and review recent behavior."
    if risk_band == "High":
        return "Trigger analyst review and tighter exposure controls."
    return "Escalate immediately for risk intervention."

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 1.25rem 1.5rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    margin-bottom: 1rem;
}
.hero h1 {
    margin: 0;
    font-size: 2.25rem;
}
.hero p {
    margin-top: 0.4rem;
    color: #cbd5e1;
    font-size: 1rem;
}
.kpi-card {
    background: #f8fafc;
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
}
.result-card {
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    background: white;
}
.small-note {
    color: #64748b;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>AMEX Credit Risk Early Warning System</h1>
    <p>
        Production-ready credit risk dashboard for real-time default prediction, threshold optimisation, and explainable decision support.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Top KPI row
# -----------------------------
best_model = metrics.get("best_model", "LightGBM")
lgb_auc = safe_metric(metrics, "lightgbm", "roc_auc")
lgb_f1 = safe_metric(metrics, "lightgbm", "f1")
log_auc = safe_metric(metrics, "logistic_regression", "roc_auc")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Best Model", best_model)
k2.metric("LightGBM ROC-AUC", f"{lgb_auc:.3f}")
k3.metric("LightGBM F1", f"{lgb_f1:.3f}")
k4.metric("Logistic ROC-AUC", f"{log_auc:.3f}")

st.caption("Use the Predict tab for individual scoring, Thresholds for operating-point review, and Explainability for feature drivers.")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Predict", "Explainability", "Thresholds"])

with tab1:
    c1, c2 = st.columns([1.1, 1])

    with c1:
        st.subheader("Model Summary")
        summary_df = pd.DataFrame([
            {
                "Model": "Logistic Regression",
                "ROC-AUC": safe_metric(metrics, "logistic_regression", "roc_auc"),
                "Accuracy": safe_metric(metrics, "logistic_regression", "accuracy"),
                "Precision": safe_metric(metrics, "logistic_regression", "precision"),
                "Recall": safe_metric(metrics, "logistic_regression", "recall"),
                "F1": safe_metric(metrics, "logistic_regression", "f1"),
            },
            {
                "Model": "LightGBM",
                "ROC-AUC": safe_metric(metrics, "lightgbm", "roc_auc"),
                "Accuracy": safe_metric(metrics, "lightgbm", "accuracy"),
                "Precision": safe_metric(metrics, "lightgbm", "precision"),
                "Recall": safe_metric(metrics, "lightgbm", "recall"),
                "F1": safe_metric(metrics, "lightgbm", "f1"),
            },
        ])
        st.dataframe(summary_df, use_container_width=True)

    with c2:
        st.subheader("Interpretation")
        st.markdown("""
- **Low risk:** behavior appears stable relative to the model's learned patterns.
- **Medium risk:** some signals are elevated and warrant closer monitoring.
- **High risk:** strong warning signals; manual review is recommended.
- **Critical risk:** immediate intervention may be appropriate.
        """)
        st.markdown(
            '<p class="small-note">This dashboard supports decision-making; it should complement, not replace, analyst judgment.</p>',
            unsafe_allow_html=True,
        )

with tab2:
    st.subheader("Single Customer Risk Prediction")
    st.write("Enter a small set of key engineered features. Advanced fields can be expanded if needed.")

    # Top features first
    default_top_features = [
        "P_2_latest",
        "B_11_latest",
        "D_39_latest",
        "S_3_avg",
        "P_2_delta",
        "B_11_delta",
        "D_39_max",
        "n_statements",
    ]
    top_features = [f for f in default_top_features if f in feature_columns]
    advanced_features = [f for f in feature_columns if f not in top_features]

    user_inputs = {}

    with st.form("prediction_form"):
        cols = st.columns(2)
        for idx, feature in enumerate(top_features):
            with cols[idx % 2]:
                user_inputs[feature] = st.number_input(
                    feature,
                    value=0.0,
                    step=0.01,
                    format="%.4f"
                )

        with st.expander("Advanced Inputs"):
            adv_cols = st.columns(2)
            for idx, feature in enumerate(advanced_features[:16]):  # keep it manageable
                with adv_cols[idx % 2]:
                    user_inputs[feature] = st.number_input(
                        feature,
                        value=0.0,
                        step=0.01,
                        format="%.4f"
                    )

        submitted = st.form_submit_button("Predict Risk")

    if submitted:
        risk_score, predicted_class, risk_band = predict_score(user_inputs)

        r1, r2, r3 = st.columns(3)
        r1.metric("Risk Score", f"{risk_score:.4f}")
        r2.metric("Predicted Class", predicted_class)
        r3.metric("Risk Band", risk_band)

        st.markdown(
            f"""
            <div class="result-card" style="border-left: 8px solid {risk_band_color(risk_band)};">
                <h4 style="margin-bottom:0.3rem;">Decision Guidance</h4>
                <p style="margin:0;">
                    <strong>{risk_band}</strong> risk detected.
                    {recommendation_from_band(risk_band)}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab3:
    st.subheader("Top Feature Drivers")

    if importance_df is not None and not importance_df.empty:
        top_n = st.slider("Number of features to display", 5, 20, 10)
        chart_df = importance_df.head(top_n).sort_values("importance", ascending=True)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(chart_df["feature"], chart_df["importance"])
        ax.set_title("Top Feature Importances")
        ax.set_xlabel("Importance")
        ax.set_ylabel("")
        st.pyplot(fig)

        st.dataframe(importance_df.head(20), use_container_width=True)
    else:
        st.info("Feature importance file not available.")

with tab4:
    st.subheader("Threshold Tuning")

    if threshold_df is not None and not threshold_df.empty:
        display_df = threshold_df.copy()

        # highlight best F1 row
        best_idx = display_df["f1"].idxmax()
        recommended_threshold = display_df.loc[best_idx, "threshold"]

        st.metric("Recommended Threshold", f"{recommended_threshold:.2f}")
        st.caption("Recommended here as the best F1 operating point on the saved validation results.")

        st.dataframe(display_df, use_container_width=True)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(display_df["threshold"], display_df["precision"], label="Precision")
        ax.plot(display_df["threshold"], display_df["recall"], label="Recall")
        ax.plot(display_df["threshold"], display_df["f1"], label="F1")
        ax.axvline(recommended_threshold, linestyle="--")
        ax.set_title("Threshold Trade-offs")
        ax.set_xlabel("Threshold")
        ax.set_ylabel("Score")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("Threshold metrics file not available.")

st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        <strong>Daniel Diala</strong> |
        <a href="https://github.com/dd4real2k/" target="_blank" style="text-decoration: none; color: #2563eb;">
            GitHub Portfolio
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
