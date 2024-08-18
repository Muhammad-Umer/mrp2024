from sklearn.model_selection import KFold
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Step 1: Define a function to create the LSTM model
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Step 2: Prepare data
X = np.array(X)
y = np.array(y)

# Step 3: Implement K-Fold Cross-Validation manually
kf = KFold(n_splits=5, shuffle=False)
cv_scores = []

for train_index, val_index in kf.split(X):
    X_train_cv, X_val_cv = X[train_index], X[val_index]
    y_train_cv, y_val_cv = y[train_index], y[val_index]

    # Reshape data for LSTM
    X_train_cv = X_train_cv.reshape((X_train_cv.shape[0], X_train_cv.shape[1], 1))
    X_val_cv = X_val_cv.reshape((X_val_cv.shape[0], X_val_cv.shape[1], 1))

    # Create and train model
    model = create_lstm_model((X_train_cv.shape[1], 1))
    model.fit(X_train_cv, y_train_cv, epochs=20, batch_size=32, verbose=0)

    # Evaluate model on validation set
    val_pred = model.predict(X_val_cv)
    mse = np.mean((val_pred - y_val_cv) ** 2)
    cv_scores.append(mse)

# Step 4: Calculate and print cross-validation scores
mean_cv_score = np.mean(cv_scores)
print(f"Mean Cross-Validation MSE: {mean_cv_score}")
