import os
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
from google.cloud import bigquery
from google.oauth2 import service_account
from sklearn import set_config
from dotenv import load_dotenv

# ==========================
# Create Directory (if not exists)
# ==========================
def create_directory(directory_path):
    """
    Create a directory if it does not exist.

    :param directory_path: Path of the directory to be created
    """
    os.makedirs(directory_path, exist_ok=True)
    print(f"✅ Directory checked/created: {directory_path}")

# ==========================
# 1️⃣ Set Up Google Cloud Authentication
# ==========================
def setup_google_auth(key_path):
    """
    Set up Google Cloud authentication using a service account key.

    :param key_path: Path to the service account JSON key file
    :return: BigQuery client object
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    print(f"✅ Google Cloud authentication set with key: {key_path}")
    return client

# ==========================
# 2️⃣ Create BigQuery Dataset (If Not Exists)
# ==========================
def create_bigquery_dataset(client, dataset_id):
    """
    Check if a BigQuery dataset exists; if not, create it.

    :param client: BigQuery client
    :param dataset_id: Dataset ID
    """
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)  # Check if dataset exists
        print(f"✅ Dataset {dataset_id} already exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        client.create_dataset(dataset)
        print(f"✅ Dataset {dataset_id} created.")

# ==========================
# 3️⃣ Create BigQuery Table (If Not Exists)
# ==========================
def create_bigquery_table(client, dataset_id, table_id, schema):
    """
    Check if a BigQuery table exists; if not, create it.

    :param client: BigQuery client
    :param dataset_id: Dataset ID
    :param table_id: Table ID
    :param schema: Table schema
    """
    table_ref = client.dataset(dataset_id).table(table_id)
    try:
        client.get_table(table_ref)  # Check if table exists
        print(f"✅ Table {table_id} already exists.")
    except Exception:
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"✅ Table {table_id} created.")

# ==========================
# 4️⃣ Load & Clean CSV Data
# ==========================
def load_and_clean_data(csv_file_path, selected_columns):
    """
    Load CSV data, select specific columns, and clean it.

    :param csv_file_path: Path to the CSV file
    :param selected_columns: List of columns to keep
    :return: Cleaned DataFrame
    """
    df = pd.read_csv(csv_file_path, on_bad_lines="skip")  # Read CSV
    df_selected = df[selected_columns]  # Select required columns

    # Convert numeric columns
    numeric_columns = ["price", "price_difference", "price_percent_change", "price_changed"]
    for col in numeric_columns:
        df_selected[col] = pd.to_numeric(df_selected[col], errors="coerce")

    # Convert date column
    df_selected["life_span_date"] = pd.to_datetime(df_selected["life_span_date"], errors="coerce")

    # Drop rows where reference_code is missing
    df_selected.dropna(subset=["reference_code"], inplace=True)

    print(f"✅ Data cleaned: {df_selected.shape[0]} rows, {df_selected.shape[1]} columns.")
    return df_selected

# ==========================
# 5️⃣ Upload Data to BigQuery
# ==========================
def upload_data_to_bigquery(client, dataset_id, table_id, df):
    """
    Upload a Pandas DataFrame to a BigQuery table.

    :param client: BigQuery client
    :param dataset_id: Dataset ID
    :param table_id: Table ID
    :param df: DataFrame to upload
    """
    table_ref = client.dataset(dataset_id).table(table_id)
    job = client.load_table_from_dataframe(df, table_ref)
    job.result()  # Wait for upload completion

    print(f"✅ Loaded {job.output_rows} rows into {dataset_id}.{table_id}.")

# ==========================
# 6️⃣ Main Execution
# ==========================
if __name__ == "__main__":
      # Step 1: Create necessary directories
    create_directory("/Users/20766/Desktop/Business Project/data")
    
    
    load_dotenv()

    # Access environment variables
    key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.getenv("BQ_PROJECT_ID")
    dataset_id = os.getenv("BQ_DATASET_ID")
    table_id = os.getenv("BQ_TABLE_ID")
    csv_file_path = os.getenv("CSV_FILE_PATH")

    print(key_path, project_id, dataset_id, table_id, csv_file_path)

    # Define table schema
    
    schema = [ 
    bigquery.SchemaField("uid", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("brand", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("url", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("price", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("currency", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("image_url", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("collection", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("reference_code", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("life_span_date", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("life_span", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("price_before", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("price_difference", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("price_percent_change", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("price_changed", "BOOLEAN", mode="NULLABLE"),
    bigquery.SchemaField("Exchange_Rate", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("price_eur", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("price_difference_eur", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("price_before_eur", "FLOAT", mode="NULLABLE"),
    ]

    # Define required columns
    selected_columns = [
        "uid", "brand", "url", "price", "currency", "image_url", "collection",
        "reference_code", "life_span_date", "life_span", "price_before",
        "price_difference", "price_percent_change", "price_changed"
    ]

    # Step 1: Set up authentication
    client = setup_google_auth(key_path)

    # Step 2: Create dataset and table
    create_bigquery_dataset(client, dataset_id)
    create_bigquery_table(client, dataset_id, table_id, schema)

    # Step 3: Load, clean, and upload data
    df_cleaned = load_and_clean_data(csv_file_path, selected_columns)
    upload_data_to_bigquery(client, dataset_id, table_id, df_cleaned)




