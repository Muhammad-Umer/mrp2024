from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

# Step 1: Preparing Data
processed_data['direction'] = np.where(processed_data['generated_price'].shift(-1) > processed_data['generated_price'], 1, 0)

# Ensure consistent dropping of NaNs across both features and target
features = ['roc_7', 'roc_30', 'ma_7', 'ma_30', 'direction']
data = processed_data[features].dropna().reset_index(drop=True)

# Splitting features and target after dropping NaNs
X_direction = data[['roc_7', 'roc_30', 'ma_7', 'ma_30']]
y_direction = data['direction']

# Step 2: Splitting Data
X_train_dir, X_test_dir, y_train_dir, y_test_dir = train_test_split(X_direction, y_direction, test_size=0.2, shuffle=False)

# Step 3: Logistic Regression
log_reg = LogisticRegression()
log_reg.fit(X_train_dir, y_train_dir)
y_pred_dir_log = log_reg.predict(X_test_dir)

# Step 4: Random Forest Classifier
rf_clf = RandomForestClassifier()
rf_clf.fit(X_train_dir, y_train_dir)
y_pred_dir_rf = rf_clf.predict(X_test_dir)

# Step 5: Evaluation
precision_log = precision_score(y_test_dir, y_pred_dir_log)
recall_log = recall_score(y_test_dir, y_pred_dir_log)
f1_log = f1_score(y_test_dir, y_pred_dir_log)

precision_rf = precision_score(y_test_dir, y_pred_dir_rf)
recall_rf = recall_score(y_test_dir, y_pred_dir_rf)
f1_rf = f1_score(y_test_dir, y_pred_dir_rf)

print(f"Logistic Regression - Precision: {precision_log}, Recall: {recall_log}, F1-Score: {f1_log}")
print(f"Random Forest - Precision: {precision_rf}, Recall: {recall_rf}, F1-Score: {f1_rf}")
