import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Step 1: LSTM Confidence Interval
pred_std = np.std(y_pred - y_test)  # Standard deviation of the prediction errors
conf_interval = norm.interval(0.95, loc=y_pred, scale=pred_std)

# Step 2: Classification and Regression Confidence Measures
rf_probs = rf_clf.predict_proba(X_test_dir)
rf_confidence = np.max(rf_probs, axis=1)

svr_std = np.std(y_pred_time_svr - y_test_time)
svr_confidence_interval = norm.interval(0.95, loc=y_pred_time_svr, scale=svr_std)

# Flatten the confidence intervals
conf_interval_lower = conf_interval[0].flatten()
conf_interval_upper = conf_interval[1].flatten()

# Ensure that y_pred and confidence intervals have the same length and are 1D
y_pred = y_pred.flatten()

# Create a figure and axis objects with subplots
fig, ax = plt.subplots(figsize=(14, 7))

# Plot the LSTM predictions with a thicker line for better visibility
ax.plot(processed_data['date'].iloc[-len(y_pred):], y_pred, label='Predicted Price', color='blue', linewidth=2)

# Plot the confidence intervals with a different color and slightly transparent fill
ax.fill_between(processed_data['date'].iloc[-len(y_pred):], conf_interval_lower, conf_interval_upper,
                color='orange', alpha=0.2, label='95% Confidence Interval')

# Customize the plot
ax.set_title('LSTM Predicted Prices with Confidence Intervals', fontsize=16)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Generated Price', fontsize=12)

# Add grid lines for better readability
ax.grid(True, linestyle='--', alpha=0.6)

# Customize ticks for better readability
ax.tick_params(axis='both', which='major', labelsize=10)

# Move the legend inside the plot, floating on the top right of the grid
ax.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=12, frameon=True)

# Adjust layout to make room for the plot
plt.tight_layout()

# Show the plot
plt.show()
