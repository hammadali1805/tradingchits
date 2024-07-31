import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch historical stock data
ticker = '^NSEI'
data = yf.download(ticker, period='1mo', interval='1d')

# Calculate the MACD and Signal lines
short_ema = data['Close'].ewm(span=12, adjust=False).mean()
long_ema = data['Close'].ewm(span=26, adjust=False).mean()
macd = short_ema - long_ema
signal = macd.ewm(span=9, adjust=False).mean()

# Calculate the Histogram
histogram = macd - signal

# Add MACD, Signal, and Histogram to the DataFrame
data['MACD'] = macd
data['Signal'] = signal
data['Histogram'] = histogram

# Plot the MACD, Signal, and Histogram
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(data['Close'], label='Close Price')
plt.title('Close Price')
plt.legend(loc='upper left')

plt.subplot(2, 1, 2)
plt.plot(data['MACD'], label='MACD', color='blue')
plt.plot(data['Signal'], label='Signal', color='red')
plt.bar(data.index, data['Histogram'], label='Histogram', color='gray', alpha=0.3)
plt.title('MACD Indicator')
plt.legend(loc='upper left')

plt.show()
