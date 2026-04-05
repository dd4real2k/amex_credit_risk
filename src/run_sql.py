from pathlib import Path
from src.config import PROJECT_ID, SQL_DIR
from src.bq_utils import get_bq_client, run_sql_file

SQL_FILES = [
    "01_profile_raw_data.sql",
    "02_join_labels.sql",
    "03_base_customer_features.sql",
    "04_latest_record_features.sql",
    "05_model_dataset.sql",
    "06_first_record_features.sql",
    "07_missingness_features.sql",
    "08_model_dataset_v2.sql",
]

def main():
    client = get_bq_client(PROJECT_ID)

    for file_name in SQL_FILES:
        sql_path = SQL_DIR / file_name
        print(f"Running {sql_path.name}...")
        run_sql_file(client, sql_path)
        print(f"Completed {sql_path.name}")

if __name__ == "__main__":
    main()
