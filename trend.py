import yfinance as yf
import pandas as pd
import numpy as np

# Download historical market data for ACC Ltd. (ACC.NS)
ticker = '^NSEI'
data = yf.download(ticker, period='max', interval='1d')
# Calculate True Range (TR)
data['High-Low'] = data['High'] - data['Low']
data['High-PreviousClose'] = np.abs(data['High'] - data['Close'].shift(1))
data['Low-PreviousClose'] = np.abs(data['Low'] - data['Close'].shift(1))
data['TrueRange'] = data[['High-Low', 'High-PreviousClose', 'Low-PreviousClose']].max(axis=1)

# Calculate the Average True Range (ATR) using the recursive formula
atr_period = 14

# Initialize the ATR column
data['ATR'] = np.nan

# Set the first ATR value to the mean of the initial TR values
initial_tr = data['TrueRange'].iloc[:atr_period].mean()
data.loc[data.index[atr_period - 1], 'ATR'] = initial_tr

# Calculate the ATR values using the recursive formula
for i in range(atr_period, len(data)):
    previous_atr = data['ATR'].iloc[i - 1]
    current_tr = data['TrueRange'].iloc[i]
    new_atr = ((previous_atr * (atr_period - 1)) + current_tr) / atr_period
    data.loc[data.index[i], 'ATR'] = new_atr

# Calculate the Supertrend
supertrend_multiplier = 3

data['BasicUpperBand'] = (data['High'] + data['Low']) / 2 + supertrend_multiplier * data['ATR']
data['BasicLowerBand'] = (data['High'] + data['Low']) / 2 - supertrend_multiplier * data['ATR']

# Initialize the Final Bands
data['FinalUpperBand'] = data['BasicUpperBand']
data['FinalLowerBand'] = data['BasicLowerBand']

for i in range(atr_period, len(data)):
    if data['Close'].iloc[i-1] <= data['FinalUpperBand'].iloc[i-1]:
        data.loc[data.index[i], 'FinalUpperBand'] = min(data['BasicUpperBand'].iloc[i], data['FinalUpperBand'].iloc[i-1])
    else:
        data.loc[data.index[i], 'FinalUpperBand'] = data['BasicUpperBand'].iloc[i]

    if data['Close'].iloc[i-1] >= data['FinalLowerBand'].iloc[i-1]:
        data.loc[data.index[i], 'FinalLowerBand'] = max(data['BasicLowerBand'].iloc[i], data['FinalLowerBand'].iloc[i-1])
    else:
        data.loc[data.index[i], 'FinalLowerBand'] = data['BasicLowerBand'].iloc[i]

# Determine Supertrend value
data['Supertrend'] = np.nan
data['Trend'] = np.nan

for i in range(atr_period, len(data)):
    if data['Close'].iloc[i] > data['FinalUpperBand'].iloc[i-1]:
        data.loc[data.index[i], 'Supertrend'] = data['FinalLowerBand'].iloc[i]
        data.loc[data.index[i], 'Trend'] = 'Uptrend'
    elif data['Close'].iloc[i] < data['FinalLowerBand'].iloc[i-1]:
        data.loc[data.index[i], 'Supertrend'] = data['FinalUpperBand'].iloc[i]
        data.loc[data.index[i], 'Trend'] = 'Downtrend'
    else:
        data.loc[data.index[i], 'Supertrend'] = data['Supertrend'].iloc[i-1]
        data.loc[data.index[i], 'Trend'] = data['Trend'].iloc[i-1]

# Display the final data with ATR, Supertrend, and Trend
print(data[['High', 'Low', 'Close', 'TrueRange', 'ATR', 'Supertrend', 'Trend']].tail(40))
