# Make sure you have downloaded this => !pip install Historic-Crypto

import pandas as pd
from Historic_Crypto import HistoricalData

# Function to retrieve and process data for a given cryptocurrency pair
def get_crypto_data(pair, start_date, end_date):
    # Fetch the historical data
    data = HistoricalData(pair, 86400, start_date, end_date).retrieve_data()

    # Reset the index to get the date column
    data = data.reset_index()

    # Rename the columns to match the required format
    data = data.rename(columns={'time': 'date', 'close': 'generated_price'})

    # Add the 'abbr' column
    data['abbr'] = pair

    # Select only the relevant columns
    data = data[['abbr', 'date', 'generated_price']]

    return data

# Retrieve data for each cryptocurrency pair and combine them
crypto_pairs = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'DOGE-USD', 'ADA-USD', 'AVAX-USD', 'SHIB-USD', 'DOT-USD', 'LINK-USD', 'LTC-USD']

all_data = pd.DataFrame()

for pair in crypto_pairs:
    # Get data for the first half of 2023
    data_first_half = get_crypto_data(pair, '2022-01-01-00-00', '2022-06-30-00-00')

    # Get data for the second half of 2023
    data_second_half = get_crypto_data(pair, '2022-07-01-00-00', '2022-12-31-00-00')

    # Combine both halves
    combined_data = pd.concat([data_first_half, data_second_half], ignore_index=True)

    # Append to the all_data DataFrame
    all_data = pd.concat([all_data, combined_data], ignore_index=True)

# Display the final DataFrame
print(all_data)

