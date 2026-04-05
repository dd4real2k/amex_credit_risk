from pathlib import Path

PROJECT_ID = "amex-46887"
DATASET_ID = "amex_risk"
BUCKET_NAME = "amex-risk-data-46887"
BQ_LOCATION = "US"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = PROJECT_ROOT / "sql"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

RAW_TRAIN_TABLE = f"{PROJECT_ID}.{DATASET_ID}.train_data_raw"
RAW_LABELS_TABLE = f"{PROJECT_ID}.{DATASET_ID}.train_labels_raw"
RAW_TEST_TABLE = f"{PROJECT_ID}.{DATASET_ID}.test_data_raw"

TRAIN_JOINED_TABLE = f"{PROJECT_ID}.{DATASET_ID}.train_joined"
CUSTOMER_FEATURES_BASE_TABLE = f"{PROJECT_ID}.{DATASET_ID}.customer_features_base"
CUSTOMER_FEATURES_LATEST_TABLE = f"{PROJECT_ID}.{DATASET_ID}.customer_features_latest"
