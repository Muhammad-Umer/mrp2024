import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)  # Adjust the width to prevent wrapping

# Function to detect pump and dump events using initial and final prices and volumes
def detect_pump_and_dump(df, price_threshold=0.3, volume_threshold=0.3):
    # Calculate percentage change based on initial and final prices
    df['price_change'] = (df['final_price'] - df['initial_price']) / df['initial_price']
    df['volume_change'] = (df['final_volume'] - df['initial_volume']) / df['initial_volume']

    # Handle cases where the initial price or volume is zero to prevent division by zero
    df['price_change'] = np.where(df['initial_price'] == 0, np.nan, df['price_change'])
    df['volume_change'] = np.where(df['initial_volume'] == 0, np.nan, df['volume_change'])

    # Optionally, fill NaN values with zero or another placeholder
    df['price_change'] = df['price_change'].fillna(0)
    df['volume_change'] = df['volume_change'].fillna(0)

    # Identify pump and dump events
    df['pump_and_dump'] = np.where(
        (df['price_change'] > price_threshold) & (df['volume_change'] > volume_threshold), 1, 0
    )

    # Filter to only include rows where a pump and dump event was detected
    pump_and_dump_events = df[df['pump_and_dump'] == 1]

    # Calculate a score to rank the pump and dump events by their severity
    pump_and_dump_events['pump_and_dump_score'] = pump_and_dump_events['price_change'] * pump_and_dump_events['volume_change']

    return pump_and_dump_events

# Configurable number of top pump and dump events to plot
N = 10  # You can change this to 20, 30, etc.

# Apply the detection algorithm to the dataset
df_pump = df_clean

# Sort the DataFrame by date to ensure correct chronological order
df_pump = df_pump.sort_values(by='date_taken')

# Create initial and final price and volume columns
df_pump['initial_price'] = df_pump['price'].shift(1)  # Previous day's price
df_pump['final_price'] = df_pump['price']  # Current day's price
df_pump['initial_volume'] = df_pump['volume24hrs'].shift(1)  # Previous day's volume
df_pump['final_volume'] = df_pump['volume24hrs']  # Current day's volume

# Apply the detection algorithm to the dataset
df_pump = detect_pump_and_dump(df_pump)

# Select the top N greatest pump and dump events based on the pump_and_dump_score
top_pump_and_dump_events = df_pump.nlargest(N, 'pump_and_dump_score')

print(f"Top {N} Greatest Pump and Dump Events:")
print(top_pump_and_dump_events[['name', 'date_taken', 'initial_price', 'final_price', 'price_change', 'initial_volume', 'final_volume', 'volume_change', 'pump_and_dump_score']])

# Plotting top N greatest pump and dump events
plt.figure(figsize=(14, 10))

# Plot price changes
plt.subplot(2, 1, 1)
plt.bar(top_pump_and_dump_events['date_taken'], top_pump_and_dump_events['price_change'], color='blue')
plt.yscale('symlog')  # Use symmetrical logarithmic scale to handle large variations
plt.title(f'Top {N} Greatest Pump and Dump Events - Price Change')
plt.xlabel('Date')
plt.ylabel('Price Change (%)')

# Plot volume changes
plt.subplot(2, 1, 2)
plt.bar(top_pump_and_dump_events['date_taken'], top_pump_and_dump_events['volume_change'], color='orange')
plt.yscale('symlog')  # Use symmetrical logarithmic scale to handle large variations
plt.title(f'Top {N} Greatest Pump and Dump Events - Volume Change')
plt.xlabel('Date')
plt.ylabel('Volume Change (%)')

plt.tight_layout()
plt.show()
