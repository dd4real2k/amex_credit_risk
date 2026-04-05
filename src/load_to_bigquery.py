from google.cloud import bigquery

PROJECT_ID = "amex-46887"
DATASET_ID = "amex_risk"
BUCKET = "gs://amex-risk-data-46887/raw"

client = bigquery.Client(project=PROJECT_ID)

tables = {
    "train_data_raw": f"{BUCKET}/train_data.csv",
    "train_labels_raw": f"{BUCKET}/train_labels.csv",
    "test_data_raw": f"{BUCKET}/test_data.csv",
    "sample_submission_raw": f"{BUCKET}/sample_submission.csv",
}

for table_name, uri in tables.items():
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows:,} rows into {table_id}")
