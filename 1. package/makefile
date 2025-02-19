# Define environment variables
ENV_FILE=.env

# Define Python scripts
FETCH_EXCHANGE_RATES=python API_exchange_rates.py
CLEAN_DATA=python clean_data_bigquery.py
UPLOAD_BIGQUERY=python Upload_to_Bigquery.py
RUN_MODEL=python Model.py

# Define the default target
.PHONY: run_all install install_dev setup fetch clean upload model

# Load environment variables
include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))


install:
    pip install -r requirements.txt

install_dev:
    pip install -e .

setup:
    python setup.py install


# Run all steps sequentially
run_all: fetch clean upload model
    @echo "✅ All tasks completed successfully!"

# Fetch exchange rates
fetch:
    @echo "🔄 Fetching exchange rates..."
    @$(FETCH_EXCHANGE_RATES)
    @echo "✅ Exchange rates fetched."

# Clean data
clean: fetch
    @echo "🔄 Cleaning data..."
    @$(CLEAN_DATA)
    @echo "✅ Data cleaned."

# Upload data to BigQuery
upload: clean
    @echo "🔄 Uploading data to BigQuery..."
    @$(UPLOAD_BIGQUERY)
    @echo "✅ Data uploaded to BigQuery."

# Run model
model: upload
    @echo "🔄 Running machine learning model..."
    @$(RUN_MODEL)
    @echo "✅ Model execution completed."
