from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Step 1: Creating the 'time_to_next_correction' target
processed_data['time_to_next_correction'] = processed_data['date'].diff().shift(-1).dt.total_seconds().div(3600)  # Hours till next row

# Ensure consistent dropping of NaNs across both features and target
features_timeframe = ['roc_7', 'roc_30', 'ma_7', 'ma_30', 'time_to_next_correction']
data_timeframe = processed_data[features_timeframe].dropna().reset_index(drop=True)

# Splitting features and target after dropping NaNs
X_timeframe = data_timeframe[['roc_7', 'roc_30', 'ma_7', 'ma_30']]
y_timeframe = data_timeframe['time_to_next_correction']

# Step 2: Splitting Data
X_train_time, X_test_time, y_train_time, y_test_time = train_test_split(X_timeframe, y_timeframe, test_size=0.2, shuffle=False)

# Step 3: Linear Regression
lin_reg = LinearRegression()
lin_reg.fit(X_train_time, y_train_time)
y_pred_time_lin = lin_reg.predict(X_test_time)

# Step 4: Support Vector Regression
svr = SVR(kernel='rbf')
svr.fit(X_train_time, y_train_time)
y_pred_time_svr = svr.predict(X_test_time)

# Step 5: Evaluation
mae_time_lin = mean_absolute_error(y_test_time, y_pred_time_lin)
rmse_time_lin = np.sqrt(mean_squared_error(y_test_time, y_pred_time_lin))

mae_time_svr = mean_absolute_error(y_test_time, y_pred_time_svr)
rmse_time_svr = np.sqrt(mean_squared_error(y_test_time, y_pred_time_svr))

print(f"Linear Regression - MAE: {mae_time_lin}, RMSE: {rmse_time_lin}")
print(f"SVR - MAE: {mae_time_svr}, RMSE: {rmse_time_svr}")
