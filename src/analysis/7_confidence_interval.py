from scipy.stats import norm

# Step 1: LSTM Confidence Interval
pred_std = np.std(y_pred - y_test)  # Standard deviation of the prediction errors
conf_interval = norm.interval(0.95, loc=y_pred, scale=pred_std)

# Step 2: Classification and Regression Confidence Measures
rf_probs = rf_clf.predict_proba(X_test_dir)
rf_confidence = np.max(rf_probs, axis=1)

svr_std = np.std(y_pred_time_svr - y_test_time)
svr_confidence_interval = norm.interval(0.95, loc=y_pred_time_svr, scale=svr_std)
