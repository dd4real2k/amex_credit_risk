from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
from google.cloud import bigquery
from lightgbm import LGBMClassifier
from pandas.api.types import is_numeric_dtype
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from src.evaluate import (
    evaluate_classifier,
    print_diagnostics,
    save_metrics,
    threshold_table,
)

PROJECT_ID = "amex-46887"
DATASET_ID = "amex_risk"
TABLE_NAME = "model_dataset_v2"
MODELS_DIR = Path("models")
BQ_LOCATION = "US"
MODEL_VERSION = "v1"

ROOT_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT_DIR / "models" / MODEL_VERSION



def load_training_data() -> pd.DataFrame:
    """Load the engineered training dataset from BigQuery."""
    client = bigquery.Client(project=PROJECT_ID, location=BQ_LOCATION)
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
    """
    return client.query(query).to_dataframe()


def build_feature_matrix(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Build a clean numeric feature matrix and target vector."""
    drop_cols = [
        "customer_ID",
        "target",
        "latest_statement_date",
        "first_statement_date",
    ]

    X = df.drop(columns=drop_cols, errors="ignore").copy()
    y = df["target"].copy()

    numeric_cols = [col for col in X.columns if is_numeric_dtype(X[col])]
    X = X[numeric_cols].copy()

    # Simple missing value handling for baseline modelllling
    X = X.fillna(-999)

    return X, y


def train_logistic_regression(X_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression:
    """Train the baseline Logistic Regression model."""
    model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        solver="liblinear",
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def train_lightgbm(X_train: pd.DataFrame, y_train: pd.Series) -> LGBMClassifier:
    """Train the LightGBM model."""
    model = LGBMClassifier(
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def save_artifacts(
    best_model,
    feature_columns: list[str],
    metrics: dict,
    threshold_df: pd.DataFrame,
    feature_importance_df: Optional[pd.DataFrame] = None
) -> None:
    """Save model artifacts for deployment."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_model, MODELS_DIR / "model.pkl")
    joblib.dump(feature_columns, MODELS_DIR / "feature_columns.pkl")

    save_metrics(metrics, MODELS_DIR / "metrics.json")
    threshold_df.to_csv(MODELS_DIR / "threshold_metrics.csv", index=False)

    if feature_importance_df is not None:
        feature_importance_df.to_csv(MODELS_DIR / "feature_importance.csv", index=False)


def main():
    print("Loading training data from BigQuery...")
    df = load_training_data()
    print(f"Loaded dataset shape: {df.shape}")

    print("Building feature matrix...")
    X, y = build_feature_matrix(df)
    print(f"Feature matrix shape: {X.shape}")
    print(f"Target shape: {y.shape}")

    X_train, X_valid, y_train, y_valid = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("Training Logistic Regression...")
    log_model = train_logistic_regression(X_train, y_train)
    log_preds = log_model.predict(X_valid)
    log_probs = log_model.predict_proba(X_valid)[:, 1]
    log_metrics = evaluate_classifier(y_valid, log_preds, log_probs, "Logistic Regression")

    print("Training LightGBM...")
    lgb_model = train_lightgbm(X_train, y_train)
    lgb_preds = lgb_model.predict(X_valid)
    lgb_probs = lgb_model.predict_proba(X_valid)[:, 1]
    lgb_metrics = evaluate_classifier(y_valid, lgb_preds, lgb_probs, "LightGBM")

    results_df = pd.DataFrame([log_metrics, lgb_metrics]).sort_values(
        "roc_auc", ascending=False
    )
    print("\nModel comparison:")
    print(results_df.to_string(index=False))

    print("\nLightGBM diagnostics:")
    print_diagnostics(y_valid, lgb_preds)

    threshold_df = threshold_table(y_valid, lgb_probs)

    feature_importance_df = pd.DataFrame(
        {
            "feature": X.columns,
            "importance": lgb_model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    if lgb_metrics["roc_auc"] >= log_metrics["roc_auc"]:
        best_model = lgb_model
        best_model_name = "LightGBM"
        best_feature_importance_df = feature_importance_df
    else:
        best_model = log_model
        best_model_name = "Logistic Regression"
        best_feature_importance_df = None

    metrics_payload = {
        "logistic_regression": log_metrics,
        "lightgbm": lgb_metrics,
        "best_model": best_model_name,
        "model_version": MODEL_VERSION,
        "training_table": f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}",
        "n_features": len(X.columns),
    }

    save_artifacts(
        best_model=best_model,
        feature_columns=list(X.columns),
        metrics=metrics_payload,
        threshold_df=threshold_df,
        feature_importance_df=best_feature_importance_df,
    )

    print(f"\nArtifacts saved to: {MODELS_DIR}")

if __name__ == "__main__":
    main()
