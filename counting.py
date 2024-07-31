import yfinance as yf
import pandas as pd
import pandas_ta as ta
import math

# Define the ticker and the date range
ticker = "^NSEI"

# Fetch the data
data = yf.download(ticker, interval='5m', period='max')
print(data)
