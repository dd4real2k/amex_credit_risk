from pathlib import Path

import joblib
import pandas as pd
from pandas.api.types import is_numeric_dtype
from google.cloud import bigquery
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier

from src.evaluate import evaluate_classifier, threshold_table, save_metrics, print_diagnostics

PROJECT_ID = "amex-46887"
DATASET_ID = "amex_risk"
TABLE_NAME = "model_dataset_v2"
MODELS_DIR = Path("models")


def load_training_data() -> pd.DataFrame:
    client = bigquery.Client(project=PROJECT_ID, location="US")
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
    """
    df = client.query(query).to_dataframe()
    return df


def build_feature_matrix(df: pd.DataFrame):
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

    X = X.fillna(-999)

    return X, y


def train_logistic_regression(X_train, y_train):
    model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        solver="liblinear",
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def train_lightgbm(X_train, y_train):
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


def save_artifacts(best_model, feature_columns, metrics, threshold_df, feature_importance_df=None):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_model, MODELS_DIR / "best_model.pkl")
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

    results_df = pd.DataFrame([log_metrics, lgb_metrics]).sort_values("roc_auc", ascending=False)
    print("\nModel comparison:")
    print(results_df)

    print("\nLightGBM diagnostics:")
    print_diagnostics(y_valid, lgb_preds)

    threshold_df = threshold_table(y_valid, lgb_probs)

    feature_importance_df = pd.DataFrame(
        {
            "feature": X.columns,
            "importance": lgb_model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    metrics_payload = {
        "logistic_regression": log_metrics,
        "lightgbm": lgb_metrics,
        "best_model": "LightGBM" if lgb_metrics["roc_auc"] >= log_metrics["roc_auc"] else "Logistic Regression",
    }

    best_model = lgb_model if lgb_metrics["roc_auc"] >= log_metrics["roc_auc"] else log_model

    save_artifacts(
        best_model=best_model,
        feature_columns=list(X.columns),
        metrics=metrics_payload,
        threshold_df=threshold_df,
        feature_importance_df=feature_importance_df if best_model == lgb_model else None,
    )

    print("\nArtifacts saved in models/")

if __name__ == "__main__":
    main()
