import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Input, LSTM, Dense

# Load historical stock data (replace with actual data)
df = pd.read_csv("./backend/nvda_stock.csv")  # Ensure this CSV has a "Close" column

# Normalize Data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df["Close"].values.reshape(-1, 1))

# Prepare Training Data
X, y = [], []
for i in range(60, len(scaled_data)):
    X.append(scaled_data[i-60:i])
    y.append(scaled_data[i])

X, y = np.array(X), np.array(y)

# Build LSTM Model with explicit Input layer
inputs = Input(shape=(60, 1), name="input_layer")
x = LSTM(50, return_sequences=True)(inputs)
x = LSTM(50)(x)
outputs = Dense(1)(x)

model = tf.keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(X, y, epochs=10, batch_size=32)

# Save Model
model.save("lstm_model.h5")
print("✅ Model Saved Successfully!")