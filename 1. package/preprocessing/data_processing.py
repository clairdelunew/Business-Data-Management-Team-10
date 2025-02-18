#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:45:51 2025

@author: qianqian
"""
### Step 1:
# Use file 2.1 Webscrap_result_panerai_all_cleaned.csv and file 3. API-exchange_rates.csv to do currency conversion
prices_df = pd.read_csv("2.1 Webscrap_result_panerai_all_cleaned.csv")
exchange_rates_df = pd.read_csv("3. API-exchange_rates.csv")

# Make sure the exchange rate is a floating number
exchange_rates_df["Exchange Rate"] = exchange_rates_df["Exchange Rate"].astype(float)

# analyze price, remove the ",", and transform to floating number
prices_df["price.1"] = prices_df["price.1"].astype(str).str.replace(",", "").astype(float)

# merge through mapping Currency and currency， add exchange info
merged_df = prices_df.merge(exchange_rates_df, left_on="currency", right_on="Currency", how="left")

# calculate the price (original price * exchange rate)
merged_df["price_eur"] = merged_df["price.1"] * merged_df["Exchange Rate"]

# delete the column 'Currency' 
merged_df.drop(columns=["Currency"], inplace=True)

# save file
merged_df.to_csv("converted_prices_scrape.csv", index=False)

print("Save file as converted_prices_scrape.csv")


### Step2:
# Use file 1. Bigquery-edhec-business-management.csv and file 3. API-exchange_rates.csv to do currency conversion
pricesbq_df = pd.read_csv("1. Bigquery-edhec-business-management.csv")
exchange_rates_df = pd.read_csv("3. API-exchange_rates.csv")

# Make sure exchange_rates_df["Exchange Rate"] is a float
exchange_rates_df["Exchange Rate"] = pd.to_numeric(exchange_rates_df["Exchange Rate"], errors="coerce")

# Price processing: remove commas and convert to float
pricesbq_df["price"] = pd.to_numeric(pricesbq_df["price"].astype(str).str.replace(",", ""), errors="coerce")
pricesbq_df["price_before"] = pd.to_numeric(pricesbq_df["price_before"].astype(str).str.replace(",", ""), errors="coerce")
pricesbq_df["price_difference"] = pd.to_numeric(pricesbq_df["price_difference"].astype(str).str.replace(",", ""), errors="coerce")

# merge
merged_df = pricesbq_df.merge(exchange_rates_df, left_on="currency", right_on="Currency", how="left")

# Calculate price (original price * exchange rate)
merged_df["price_eur"] = merged_df["price"] * merged_df["Exchange Rate"]
merged_df["price_difference_eur"] = merged_df["price_difference"] * merged_df["Exchange Rate"]
merged_df["price_before_eur"] = merged_df["price_before"] * merged_df["Exchange Rate"]

# delete 'Currency'
merged_df.drop(columns=["Currency"], inplace=True)

# save file
merged_df.to_csv("converted_prices_bigquery.csv", index=False)
print("Save file as converted_prices_bigquery.csv")

### Step3: Merge two dataset from bigquery and scrape

# read data
scrape_df = pd.read_csv("converted_prices_scrape.csv")
big_query_df = pd.read_csv("converted_prices_bigquery.csv")

# Add suffix to columns
scrape_df.columns = [col + '_scrape' for col in scrape_df.columns]
big_query_df.columns = [col + '_bigquery' for col in big_query_df.columns]


# Create final_df, which contains the columns of big_query_df and scrape_df, and is initialized to empty
final_df = big_query_df.copy()


# Add columns of scrape_df (initial data is empty)
for col in scrape_df.columns:
    final_df[col] = None

# Merge data based on reference_code
# Assume that reference_code is unique and exists in both data frames
final_df = pd.merge(final_df, scrape_df[['reference_code_scrape', 'domain_scrape', 'config_name_scrape', 'start_url_scrape', 'date_scrape', 'brand_scrape']], 
                     left_on='reference_code_bigquery', 
                     right_on='reference_code_scrape', 
                     how='left')


# Add unmatched scrape_df data to final_df at the end
# Find reference_code that is not matched in big_query_df
no_match_scrape_df = scrape_df[~scrape_df['reference_code_scrape'].isin(final_df['reference_code_bigquery'])]

# Add these unmatched data to final_df
final_df = pd.concat([final_df, no_match_scrape_df], ignore_index=True)


# Delete identical duplicate rows
final_df = final_df.drop_duplicates()

# Delete columns with all null values
final_df = final_df.dropna(axis=1, how="all")


# . Delete duplicate columns ending with `_y`, and keep `_x` first
cols_to_drop = [col for col in final_df.columns if col.endswith('_y')]
final_df = final_df.drop(columns=cols_to_drop, errors='ignore')

#  Remove the extra suffix '_x' from the column name
final_df.columns = final_df.columns.str.replace('_x$', '', regex=True)

# remove duplicates
final_df = final_df.drop_duplicates()

# check
#print(final_df.info())
### Save final file
final_df.to_csv("final_data.csv", index=False)
