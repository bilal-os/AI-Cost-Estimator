# Import libraries
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import requests
from io import StringIO
import matplotlib.pyplot as plt
import pickle

# Fetch multiple datasets
urls = [
    "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/cocomo81-tS1OBDffXBAIx4KKZKqK2SK9b5JtZn.csv",
    # Add additional dataset URLs here
]
data_frames = [pd.read_csv(StringIO(requests.get(url).text)) for url in urls]

# Combine datasets
data = pd.concat(data_frames, ignore_index=True)

# Preprocess data
X = data.drop(columns=['2040'])  # Replace '2040' with target column name
y = data['2040']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features and target
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)
y_train_scaled = scaler_y.fit_transform(y_train.values.reshape(-1, 1))
y_test_scaled = scaler_y.transform(y_test.values.reshape(-1, 1))

scaler_X.feature_names_in_ = X.columns.tolist()

print("X.columns",X.columns)

# Save the scalers for future use
with open('scaler_X.pkl', 'wb') as f:
    pickle.dump(scaler_X, f)
with open('scaler_y.pkl', 'wb') as f:
    pickle.dump(scaler_y, f)

# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae', 'mape'])

# Train the model
history = model.fit(
    X_train_scaled, y_train_scaled,
    epochs=1000,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Plot training history
plt.figure(figsize=(12, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Training History')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Evaluate the model
test_loss, test_mae, test_mape = model.evaluate(X_test_scaled, y_test_scaled, verbose=0)
print(f"\nTest Loss: {test_loss:.4f}, Test MAE: {test_mae:.4f}, Test MAPE: {test_mape:.2f}%")

# Predictions
predictions_scaled = model.predict(X_test_scaled)
predictions = scaler_y.inverse_transform(predictions_scaled)

# Print sample predictions
print("\nSample Predictions:")
for i in range(5):
    actual = y_test.iloc[i]
    predicted = predictions[i][0]
    print(f"Actual Effort: {actual:.2f}")
    print(f"Predicted Effort: {predicted:.2f}")
    print(f"Absolute Error: {abs(actual - predicted):.2f}")
    print("---")

# Residuals Plot
residuals = y_test.values - predictions.flatten()
plt.figure(figsize=(10, 6))
plt.scatter(predictions, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.title('Residuals Plot')
plt.xlabel('Predicted Effort')
plt.ylabel('Residuals')
plt.show()

# Feature Importance Analysis
feature_importance = np.abs(model.layers[0].get_weights()[0]).mean(axis=1)
feature_names = X.columns
plt.figure(figsize=(12, 6))
plt.bar(feature_names, feature_importance)
plt.title('Feature Importance')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Save the model
model.save('cocomo_effort_model.keras')
print("\nModel saved successfully.")
