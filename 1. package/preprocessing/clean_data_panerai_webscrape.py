
import pandas as pd
# clean the original dataset from an official brand website (scraped), the original file named “Webscrap_result_panerai_all.csv”
def clean_panerai_data_and_convert_currency(file_path, exchange_rates_df, dtypes_raw):
    """
    Cleans the Panerai dataset by:
    1. Removing empty columns
    2. Converting column data types based on DTYPES_RAW
    3. Dropping duplicate and missing values
    4. Filtering out invalid rows where key columns ('reference_code', 'price', 'collection', 'brand') contain 0 or NaN
    5. Clean and convert price column to numeric (after removing non-numeric characters)
    6. Saving the cleaned dataset as 'Panerai_cleaned.csv'
    
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
    
    # Step 3: Remove duplicate rows
    df = df.drop_duplicates()
    
    # Step 4: Filter out rows where key columns ('reference_code', 'price', 'collection', 'brand') contain 0 or NaN
    key_columns = ["reference_code", "price", "collection", "brand"]
    df = df.dropna(subset=key_columns)  # Remove rows with NaN in key columns
    df = df[~df[key_columns].isin([0]).any(axis=1)]  # Remove rows where key columns contain 0
    
    

    # Step 5: Clean and convert price column to numeric (after removing non-numeric characters)
    df["price"] = pd.to_numeric(df["price"].astype(str).str.replace(",", "").str.replace("$", ""), errors="coerce")
    
    # Make sure the exchange rate data is numeric
    exchange_rates_df["Exchange Rate"] = pd.to_numeric(exchange_rates_df["Exchange Rate"], errors="coerce")
    
    # Merge exchange rate data with cleaned data
    merged_df = df.merge(exchange_rates_df, left_on="currency", right_on="Currency", how="left")
    
    # Calculate price in EUR
    merged_df["price_eur"] = merged_df["price"] * merged_df["Exchange Rate"]

    # Delete 'Currency'
    merged_df.drop(columns=["Currency"], inplace=True)
    
    
    # Step 6: Save the cleaned dataset
    output_file = "Panerai_cleaned.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"Cleaned dataset saved as {output_file}")
    
    return merged_df

# Define the dtypes for your Panerai dataset (adjusted for your columns)
dtypes_raw = {
    "reference_code": "string",  # Reference code, string type
    "price": "float",  # Price, float type
    "currency": "string",  # Currency type, string
    "collection": "string",  # Product collection, string
    "brand": "string",  # Brand name, string
    "url": "string",  # URL, string type
    "image_url": "string",  # Image URL, string type
    "category": "string",  # Category, string
    "productMaterialCase": "string",  # Material of the case, string
    "productMaterialStrap": "string",  # Material of the strap, string
    "productSpecialEdition": "string",  # Special edition, string
    "productDisplay": "string",  # Product display, string
    "size": "string",  # Size, string
    "isAvailable": "boolean",  # Availability, boolean type
    "isSellable": "boolean",  # Sellable status, boolean type
    "date": "datetime64",  # Date, datetime format
}

# Example usage
#file_path = "/Users/qianqian/Desktop/final_project/data/original/Webscrap_result_panerai_all.csv"
#exchange_rates_df = pd.read_csv("/Users/qianqian/Desktop/final_project/data/API-exchange_rates.csv")
