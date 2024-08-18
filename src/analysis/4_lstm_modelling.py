from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Step 1: Preparing Data for LSTM
sequence_length = 7  # Define sequence length for LSTM input
X = []
y = []

for i in range(sequence_length, len(processed_data)):
    X.append(processed_data['generated_price_normalized'].values[i-sequence_length:i])
    y.append(processed_data['generated_price_normalized'].values[i])

X = np.array(X)
y = np.array(y)

# Step 2: Splitting Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Step 3: Building and Training LSTM Model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=20, batch_size=32)

# Step 4: Model Evaluation
y_pred = model.predict(X_test)
mae = np.mean(np.abs(y_pred - y_test))
rmse = np.sqrt(np.mean((y_pred - y_test) ** 2))
print(mae, rmse)
