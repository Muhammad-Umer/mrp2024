# Make sure data_retrival.py is done

import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Get unique cryptocurrencies
cryptos = all_data['abbr'].unique()

# Determine the layout of subplots
num_cryptos = len(cryptos)
cols = 2
rows = (num_cryptos // cols) + (num_cryptos % cols)

# Create subplots
fig, axes = plt.subplots(rows, cols, figsize=(14, 8))
axes = axes.flatten()

# Create a colormap
cmap = cm.get_cmap('tab10', num_cryptos)  # You can choose other colormaps like 'viridis', 'plasma', etc.

# Plot each cryptocurrency in its own subplot
for i, crypto in enumerate(cryptos):
    crypto_data = all_data[all_data['abbr'] == crypto]
    if not crypto_data.empty:
        color = cmap(i)  # Get a unique color from the colormap
        axes[i].plot(crypto_data['date'], crypto_data['generated_price'], label=crypto, color=color)
        axes[i].set_title(f"{crypto}")
        axes[i].set_xlabel("Date")
        axes[i].set_ylabel("Generated Price")
        axes[i].set_yscale('log')  # Use logarithmic scale for better visualization
    else:
        axes[i].set_visible(False)  # Hide empty subplots

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
