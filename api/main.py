import sys
from typing import List
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from src.predict import load_artifacts, predict_single

app = FastAPI(
    title="AMEX Credit Risk API",
    description="Credit Risk Early Warning System API",
    version="1.0.0"
)


class PredictionPayload(BaseModel):
    features: Dict[str, Any]

class BusinessInput(BaseModel):
    balance: float
    payments: float
    delinquency: float

def map_business_to_features(data):
    return {
        "P_2_latest": data.balance,
        "B_11_latest": data.payments,
        "D_39_latest": data.delinquency,
    }

@app.get("/health")
def health():
    model, feature_columns, metrics, threshold_df, importance_df = load_artifacts()
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "n_features": len(feature_columns),
        "available_metrics": list(metrics.keys()) if metrics else [],
    }


@app.get("/metadata")
def metadata():
    _, feature_columns, metrics, threshold_df, importance_df = load_artifacts()
    return {
        "feature_columns": feature_columns,
        "metrics": metrics,
        "has_threshold_metrics": threshold_df is not None,
        "has_feature_importance": importance_df is not None,
    }


@app.post("/predict")
def predict(payload: PredictionPayload):
    return predict_single(payload.features)

@app.post("/predict/business")
def predict_business(input: BusinessInput):
    features = map_business_to_features(input)
    return predict_single(features)

@app.post("/predict/batch")
def predict_batch(payload: List[dict]):
    results = []
    for item in payload:
        results.append(predict_single(item))
    return results
