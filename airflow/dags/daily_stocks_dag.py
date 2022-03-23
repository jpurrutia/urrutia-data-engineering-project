import os
from datetime import datetime
import pandas as pd
import yfinance as yf
import sys
import math
import requests

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from google.cloud import storage
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PROJECT_ID = os.environ.get('PROJECT_ID')
BUCKET = os.environ.get('GCP_GCS_BUCKET')

MAX_WORKERS = 9


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)



with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="0 0 * * 1-5",
    default_args=default_args,
    catchup=True,
    start_date=datetime(2022, 1, 1),
    max_active_runs=1,
    tags=['test'],
) as dag:

    download_stocks_list = BashOperator(
        task_id="download_stocks_list",
        bash_command = "python3 /opt/airflow/dags/py_scripts/get_daily_stocks.py {{ dag_run.logical_date | ds }} {{ next_ds }}",
        dag=dag,
    )

    bucket_ingest_task = PythonOperator(
        task_id="bucket_ingest",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "local_file": "/opt/airflow/stocks_{{ dag_run.logical_date | ds }}.csv",
            "object_name": "raw/stocks_data_{{ dag_run.logical_date | ds }}.csv",
        },
    )

    rm_task = BashOperator(
    task_id="rm_task",
    bash_command="rm /opt/airflow/stocks_{{ dag_run.logical_date | ds }}.csv"
    
    )


    download_stocks_list >> bucket_ingest_task >> rm_task