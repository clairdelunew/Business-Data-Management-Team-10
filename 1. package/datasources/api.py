#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 00:20:06 2025

@author: mac2
"""

import requests
import pandas as pd

# API URL for exchange rates (EUR as base currency)
url = 'https://v6.exchangerate-api.com/v6/4eb043dba172cec94fe70b22/latest/EUR'

# Making the request
response = requests.get(url)
data = response.json()

# Extract the conversion rates dictionary
conversion_rates = data["conversion_rates"]

# Convert to DataFrame
df = pd.DataFrame(list(conversion_rates.items()), columns=["Currency", "Exchange Rate"])

# Save to CSV file
csv_path = "/Users/mac2/Desktop/shuju/exchange_rates.csv"
df.to_csv(csv_path, index=False)

print(f"CSV file saved to: {csv_path}")
