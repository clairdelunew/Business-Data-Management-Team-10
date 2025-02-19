

import requests
import pandas as pd
import os
from dotenv import load_dotenv


def fetch_exchange_rates(output_file="API-exchange_rates.csv"):
    """
    Fetches exchange rates from the API and saves them as a CSV file.

    :param output_file: str, the name of the output CSV file (default: "API-exchange_rates.csv")
    :return: str, path of the saved CSV file
    """


    try:
        # Making the request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Extract the conversion rates dictionary
        conversion_rates = data.get("conversion_rates", {})

        if not conversion_rates:
            print("❌ No exchange rate data found.")
            return None

        # Convert to DataFrame
        exchange_rates_df = pd.DataFrame(list(conversion_rates.items()), columns=["Currency", "Exchange Rate"])

        output_path = os.getenv('OUTPUT_PATH', 'API_exchange_rates.csv')

        # Save to CSV
        exchange_rates_df.to_csv(output_path, index=False)
        print(f"✅ Exchange rates saved to {output_path}")

        return output_file

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching exchange rates: {e}")
        return None

# ==========================
# Main Execution
# ==========================
if __name__ == "__main__":
        # API URL for exchange rates (EUR as base currency)
    url =  os.getenv("API_URL")
    
    
    fetch_exchange_rates()

