import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Creating DataFrame
pnd_df = all_data

# Convert date to datetime
pnd_df['date'] = pd.to_datetime(pnd_df['date'])

# Calculate the percentage change in price
pnd_df['price_change'] = pnd_df.groupby('abbr')['generated_price'].pct_change() * 100

# Define thresholds for identifying pumps and dumps
pump_threshold = 10  # Example: a 10% increase is considered a pump
dump_threshold = -10  # Example: a 10% decrease is considered a dump

# Identify pump and dump events
pnd_df['pump'] = pnd_df['price_change'] > pump_threshold
pnd_df['dump'] = pnd_df['price_change'] < dump_threshold

# Mark events for visualization
pnd_df['event'] = np.where(pnd_df['pump'], 'Pump', np.where(pnd_df['dump'], 'Dump', 'None'))

# Visualization
fig, axs = plt.subplots(nrows=pnd_df['abbr'].nunique(), figsize=(10, 6 * pnd_df['abbr'].nunique()))

# If only one subplot, axs is not an array
if pnd_df['abbr'].nunique() == 1:
    axs = [axs]

# Plot for each crypto pair
for i, abbr in enumerate(pnd_df['abbr'].unique()):
    df = pnd_df[pnd_df['abbr'] == abbr]
    ax = axs[i]
    ax.plot(df['date'], df['generated_price'], label=f"{abbr} Price", color='blue')

    # Highlight Pump events
    pump_dates = df[df['event'] == 'Pump']['date']
    ax.scatter(pump_dates, df[df['event'] == 'Pump']['generated_price'], color='green', label='Pump', marker='^')

    # Highlight Dump events
    dump_dates = df[df['event'] == 'Dump']['date']
    ax.scatter(dump_dates, df[df['event'] == 'Dump']['generated_price'], color='red', label='Dump', marker='v')

    ax.set_title(f"{abbr} Pump and Dump Events")
    ax.set_xlabel("Date")
    ax.set_ylabel("Generated Price")
    ax.legend()

plt.tight_layout()
plt.show()

