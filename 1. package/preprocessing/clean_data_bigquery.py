import pandas as pd
from dotenv import load_dotenv
import os

### Clean the original dataset from Edhec-business-management
def clean_bigquery_data_and_convert_currency(file_path, exchange_rates_df, dtypes_raw):
    """
    Cleans the raw BigQuery dataset by:
    1. Removing empty columns
    2. Converting column data types based on DTYPES_RAW
    3. Dropping duplicate and missing values
    4. Filtering out invalid rows where 'reference_code', 'price', 'collection', and 'brand' contain 0 or NaN
    5. Clean and convert price column to numeric (after removing non-numeric characters)
    6. Saving the cleaned dataset as 'Bigquery-edhec-business-management_cleaned.csv'
    
    :param file_path: str, path to the raw CSV file
    :param dtypes_raw: dict, a dictionary mapping column names to data types
    """
    # Load dataset
    df = pd.read_csv(file_path)
    
    # Step 1: Remove columns that are completely empty
    df = df.dropna(axis=1, how='all')
    
    # Step 2: Convert data types based on DTYPES_RAW
    for column, dtype in dtypes_raw.items():
        if column in df.columns:
            df[column] = df[column].astype(dtype, errors='ignore')
    
    # Step 3: Remove duplicate rows and rows with any missing values
    # df = df.drop_duplicates().dropna(how="any")
    # Step 3: Remove duplicate rows
    df = df.drop_duplicates()
    
    # Step 4: Filter out rows where key columns ('reference_code', 'price', 'collection', 'brand') contain 0 or NaN
    key_columns = ["reference_code", "price", "collection", "brand"]
    df = df.dropna(subset=key_columns)  # Remove rows with NaN in key columns
    df = df[~df[key_columns].isin([0]).any(axis=1)]  # Remove rows where key columns contain 0
    

    df["price"] = pd.to_numeric(df["price"].astype(str).str.replace(",", "").str.replace("$", ""), errors="coerce")
    # Step 5: Clean and convert price column to numeric (after removing non-numeric characters)
    exchange_rates_df["Exchange Rate"] = pd.to_numeric(exchange_rates_df["Exchange Rate"], errors="coerce")
    # Merge exchange rate data with cleaned data
    merged_df = df.merge(exchange_rates_df, left_on="currency", right_on="Currency", how="left")
    # Calculate price in EUR
    merged_df["price_eur"] = merged_df["price"] / merged_df["Exchange Rate"]
    merged_df["price_difference_eur"] = merged_df["price_difference"] / merged_df["Exchange Rate"]
    merged_df["price_before_eur"] = merged_df["price_before"] / merged_df["Exchange Rate"]
    # Delete'Currency'
    merged_df.drop(columns=["Currency"], inplace=True)
    
    # Step 6: Save the cleaned dataset
    output_file = "Bigquery-edhec-business-management_cleaned.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"Cleaned dataset saved as {output_file}")
    
    return merged_df





dtypes_raw = {
    "reference_code": "string",  # Reference code, string type
    "price": "float",  # Price, float type
    "price_before": "float",  # Previous price, float type
    "price_difference": "float",  # Price difference, float type
    "currency": "string",  # Currency type, string
    "collection": "string",  # Product collection, string
    "brand": "string",  # Brand name, string
    "url": "string",  # URL, string type
    "image_url": "string",  # Image URL, string type
    "country": "string",  # Country, string type
    "life_span_date": "datetime64",  # Life span date, datetime format
    "life_span": "string",  # Life span (e.g., quarter), string type
    "price_percent_change": "float",  # Price percent change, float type
    "price_changed": "boolean",  # Whether the price has changed, boolean (True/False)
    "is_new": "boolean",  # Is the product new, boolean (True/False)
    "availability": "boolean",  # Availability (in stock), boolean type (True/False)
    "date_added": "datetime64",  # Date added, datetime format (e.g., '2021-11-30')
    "customer_rating": "float",  # Customer rating, float type (1-5 scale)
    "num_reviews": "int",  # Number of reviews, integer type
}

#Main Execution
# ==========================
if __name__ == "__main__":
   
    
    
    load_dotenv()

    # Access environment variables
    file_path = os.getenv("Original_data_path")
    
    exchange_rates_df = pd.read_csv(r"C:\Users\20766\Desktop\Business Project\1.package\preprocessing\API_exchange_rates.csv")
    

    cleaned_df = clean_bigquery_data_and_convert_currency(file_path, exchange_rates_df, dtypes_raw)
    print("✅ Data Cleaned!")
    print(cleaned_df.head())

    





