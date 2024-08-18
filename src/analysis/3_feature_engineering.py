import pandas as pd
from sklearn.preprocessing import StandardScaler

# Assuming processed_data is your DataFrame
# Step 1: Handling Missing Values
processed_data = all_data
processed_data['generated_price'].fillna(method='ffill', inplace=True)

# Step 2: Normalization
scaler = StandardScaler()
processed_data['generated_price_normalized'] = scaler.fit_transform(processed_data[['generated_price']])

# Step 3: Timestamp Conversion
processed_data['date'] = pd.to_datetime(processed_data['date'])
processed_data['day_of_week'] = processed_data['date'].dt.dayofweek
processed_data['month'] = processed_data['date'].dt.month
processed_data['is_weekend'] = processed_data['date'].dt.weekday >= 5

# Step 4: Feature Engineering
# Moving Averages
processed_data['ma_7'] = processed_data['generated_price_normalized'].rolling(window=7).mean()
processed_data['ma_30'] = processed_data['generated_price_normalized'].rolling(window=30).mean()

# Rate of Change
processed_data['roc_7'] = processed_data['generated_price_normalized'].pct_change(periods=7)
processed_data['roc_30'] = processed_data['generated_price_normalized'].pct_change(periods=30)

# Lag Features
processed_data['lag_1'] = processed_data['generated_price_normalized'].shift(1)
processed_data['lag_7'] = processed_data['generated_price_normalized'].shift(7)
processed_data['lag_30'] = processed_data['generated_price_normalized'].shift(30)
