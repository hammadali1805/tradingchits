import yfinance as yf
import pandas as pd


# Function to calculate VWAP
def calculate_vwap(data):
    # Calculate typical price
    data['Typical_Price'] = (data['High'] + data['Low'] + data['Close']) / 3
    # Calculate the VWAP
    data['VWAP'] = (data['Typical_Price'] * data['Volume']).cumsum() / data['Volume'].cumsum()
    return data

# Fetch historical stock data
ticker = '^NSEI'
data = yf.download(ticker, period='max', interval='1m')

# Calculate VWAP
data_with_vwap = calculate_vwap(data)

data_with_vwap.to_csv('data.csv')

# Display the data with VWAP
print(data_with_vwap[['VWAP']].tail())
