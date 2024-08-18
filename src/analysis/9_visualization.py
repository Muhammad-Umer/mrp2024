import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Get unique cryptocurrencies
cryptos = processed_data['abbr'].unique()

# Determine the layout of subplots
num_cryptos = len(cryptos)
cols = 2
rows = (num_cryptos // cols) + (num_cryptos % cols)

# Create subplots
fig, axes = plt.subplots(rows, cols, figsize=(14, 3 * rows))
axes = axes.flatten()

# Create a colormap
cmap = cm.get_cmap('tab10', num_cryptos)

# Loop through each cryptocurrency and plot its data
for i, crypto in enumerate(cryptos):
    crypto_data = processed_data[processed_data['abbr'] == crypto].copy()

    if len(crypto_data) >= 30:
        # Normalize and reshape the data for LSTM prediction
        X_crypto = crypto_data[['generated_price_normalized']].values
        X_crypto = np.reshape(X_crypto, (X_crypto.shape[0], 1, 1))  # Reshape to 3D for LSTM

        # Predict using the model
        y_pred_crypto = model.predict(X_crypto)

        # Calculate the confidence interval
        pred_std = np.std(y_pred_crypto - X_crypto.flatten())
        conf_interval_lower = y_pred_crypto - 1.96 * pred_std
        conf_interval_upper = y_pred_crypto + 1.96 * pred_std

        # Plotting the data
        color = cmap(i)  # Get a unique color from the colormap
        axes[i].plot(crypto_data['date'], y_pred_crypto, label=f'{crypto} Predicted', color=color)
        axes[i].fill_between(crypto_data['date'], conf_interval_lower.flatten(), conf_interval_upper.flatten(), color=color, alpha=0.3)
        axes[i].set_title(f"{crypto}")
        axes[i].set_xlabel("Date")
        axes[i].set_ylabel("Generated Price")
        axes[i].legend()
    else:
        axes[i].set_visible(False)  # Hide empty subplots if there's not enough data

# Hide any empty subplots if the number of cryptos is less than the total grid space
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
