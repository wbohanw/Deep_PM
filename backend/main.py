from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

def predict_stock_price(data):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    model = tf.keras.models.load_model("lstm_model.h5")
    prediction = model.predict(np.array([scaled_data[-60:]]))
    return scaler.inverse_transform(prediction)


app = FastAPI()

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (update for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

API_KEY = "your_alpha_vantage_api_key"

# Load Pretrained LSTM Model
model = tf.keras.models.load_model("lstm_model.h5")

# Fetch Stock Data
def get_stock_data(symbol):
    if symbol != "NVDA":
        return {"error": "Invalid Stock Symbol"}
    
    prices = []
    with open("nvda_stock.csv", "r") as file:
        next(file)  # Skip header
        for line in file:
            prices.append(float(line.split(",")[4]))  # Close price is the 5th column
    
    # Return last 60 prices in chronological order (oldest first)
    return prices[-60:]

# Predict Stock Price using LSTM
def predict_stock_price(prices):
    scaler = MinMaxScaler()
    prices_scaled = scaler.fit_transform(np.array(prices).reshape(-1, 1))
    
    # Load model inside the function to ensure fresh state
    model = tf.keras.models.load_model("lstm_model.h5", compile=False)
    prediction = model.predict(np.array([prices_scaled]))
    return scaler.inverse_transform(prediction)[0][0]

# Recommend Option Strategies
def recommend_option_strategy(stock_price):
    strategies = {
        "Straddle": (stock_price, stock_price),
        "Strangle": (stock_price - 5, stock_price + 5),
        "Call": (stock_price + 5, None),
        "Put": (stock_price - 5, None)
    }
    return strategies

@app.get("/analyze/{symbol}")
async def analyze_stock(symbol: str):
    stock_data = get_stock_data(symbol)
    if "error" in stock_data:
        return stock_data
    
    predicted_price = predict_stock_price(stock_data)
    strategies = recommend_option_strategy(predicted_price)
    
    # Get latest price as the last element in the array
    return {
        "current_price": float(stock_data[-1]),  # Now correctly gets most recent price
        "predicted_price": float(predicted_price),
        "option_strategies": {
            k: (float(v[0]), float(v[1]) if v[1] is not None else "N/A") 
            for k, v in strategies.items()
        }
    }


if __name__ == "__main__":
    stock_data = get_stock_data("NVDA")
    predicted_price = predict_stock_price(stock_data)
    print(stock_data)
    print(predicted_price)