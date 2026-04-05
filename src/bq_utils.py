from pathlib import Path
from google.cloud import bigquery
import pandas as pd

from src.config import BQ_LOCATION


def get_bq_client(project_id: str) -> bigquery.Client:
    return bigquery.Client(project=project_id, location=BQ_LOCATION)


def run_query(client: bigquery.Client, query: str):
    job = client.query(query)
    return job.result()


def query_to_dataframe(client: bigquery.Client, query: str) -> pd.DataFrame:
    return client.query(query).to_dataframe()


def load_sql_file(sql_path: Path) -> str:
    return sql_path.read_text(encoding="utf-8")


def run_sql_file(client: bigquery.Client, sql_path: Path):
    query = load_sql_file(sql_path)
    return run_query(client, query)
