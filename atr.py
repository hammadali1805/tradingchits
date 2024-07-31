import yfinance as yf
import pandas as pd

# Function to calculate True Range
def true_range(data):
    data['H-L'] = data['High'] - data['Low']
    data['H-PC'] = abs(data['High'] - data['Close'].shift(1))
    data['L-PC'] = abs(data['Low'] - data['Close'].shift(1))
    tr = data[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    return tr

# Function to calculate ATR
def average_true_range(data, period=14):
    data['TR'] = true_range(data)
    atr = data['TR'].rolling(window=period).mean()
    return atr

# Fetch historical stock data
ticker = '^NSEI'
data = yf.download(ticker, period='max', interval='1d')

# Calculate ATR
data['ATR'] = average_true_range(data)

# Display the data with ATR
print(data[['ATR']].tail())
