from pathlib import Path
import json
import joblib
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT_DIR / "models"

MODEL_PATH = MODELS_DIR / "best_model.pkl"
FEATURES_PATH = MODELS_DIR / "feature_columns.pkl"
METRICS_PATH = MODELS_DIR / "metrics.json"
THRESHOLDS_PATH = MODELS_DIR / "threshold_metrics.csv"
IMPORTANCE_PATH = MODELS_DIR / "feature_importance.csv"


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURES_PATH)

    metrics = {}
    if METRICS_PATH.exists():
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            metrics = json.load(f)

    threshold_df = pd.read_csv(THRESHOLDS_PATH) if THRESHOLDS_PATH.exists() else None
    importance_df = pd.read_csv(IMPORTANCE_PATH) if IMPORTANCE_PATH.exists() else None

    return model, feature_columns, metrics, threshold_df, importance_df


def prepare_input_dataframe(payload: dict, feature_columns: list[str]) -> pd.DataFrame:
    row = {col: payload.get(col, -999) if payload.get(col, None) not in [None, ""] else -999 for col in feature_columns}
    df = pd.DataFrame([row])
    return df


def score_to_risk_band(score: float) -> str:
    if score < 0.2:
        return "Low"
    if score < 0.5:
        return "Medium"
    if score < 0.8:
        return "High"
    return "Critical"


def predict_single(payload: dict):
    model, feature_columns, metrics, threshold_df, importance_df = load_artifacts()
    X = prepare_input_dataframe(payload, feature_columns)
    risk_score = float(model.predict_proba(X)[:, 1][0])
    predicted_class = int(risk_score >= 0.5)

    return {
        "predicted_class": predicted_class,
        "risk_score": risk_score,
        "risk_band": score_to_risk_band(risk_score),
        "model_metrics": metrics,
    }
