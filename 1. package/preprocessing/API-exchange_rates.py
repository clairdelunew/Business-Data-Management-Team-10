

import requests
import pandas as pd

# API URL for exchange rates (USD as base currency)
url = 'https://v6.exchangerate-api.com/v6/4eb043dba172cec94fe70b22/latest/EUR'

# Making the request
response = requests.get(url)
data = response.json()

# Extract the conversion rates dictionary
conversion_rates = data["conversion_rates"]

# Convert to DataFrame
exchange_rates_df = pd.DataFrame(list(conversion_rates.items()), columns=["Currency", "Exchange Rate"])

exchange_rates_df.to_csv("API-exchange_rates.csv", index=False)