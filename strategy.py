import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def strategy(symbol, interval, period, atr_period, multiplier, margin):

    # Fetch historical stock data
    ticker = symbol
    data = yf.download(ticker, period=period, interval=interval)
    data = data.reset_index()

    ####################################       MACD     ########################################################

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


    for i in range(1, len(data)):
        if data.loc[i-1, 'MACD'] < data.loc[i-1, 'Signal'] and data.loc[i, 'MACD'] >= data.loc[i, 'Signal']:
            data.loc[i, 'MACD_Signal'] = 1  # Crossed from below
        elif data.loc[i-1, 'MACD'] > data.loc[i-1, 'Signal'] and data.loc[i, 'MACD'] <= data.loc[i, 'Signal']:
            data.loc[i, 'MACD_Signal'] = -1  # Crossed from above
        else:
            data.loc[i, 'MACD_Signal'] = 0

    ##################################   SUPERTREND   ############################################################

    # Calculate True Range (TR)
    data['High-Low'] = data['High'] - data['Low']
    data['High-PreviousClose'] = np.abs(data['High'] - data['Close'].shift(1))
    data['Low-PreviousClose'] = np.abs(data['Low'] - data['Close'].shift(1))
    data['TrueRange'] = data[['High-Low', 'High-PreviousClose', 'Low-PreviousClose']].max(axis=1)

    # Calculate the Average True Range (ATR) using the recursive formula
    atr_period = atr_period

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
    supertrend_multiplier = multiplier

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
    data['Trend'] = ""
    data['Supertrend_Signal'] = 0

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


    for i in range(1, len(data)):
        if data.loc[i-1, 'Trend'] == 'Downtrend' and data.loc[i, 'Trend'] == 'Uptrend':
            data.loc[i, 'Supertrend_Signal'] = 1
        elif data.loc[i-1, 'Trend'] == 'Uptrend' and data.loc[i, 'Trend'] == 'Downtrend':
            data.loc[i, 'Supertrend_Signal'] = -1
        else:
            data.loc[i, 'Supertrend_Signal'] = 0

    #####################################################################################################################

    data.to_csv("data.csv")
    data = data.to_dict(orient='records')
    margin = margin
    trades = []
    long = None
    short = None
    for i, candle in enumerate(data):
        if i < margin+1:
            continue

        if candle['Supertrend_Signal']==1:
            if short:
                trades.append({"type": "short", "id": short[0], "profit": candle['Close']>short[1]['Close']})
                short=None
            for x in data[i-margin : i+1]:
                if x['MACD_Signal'] == 1 and x['MACD']<0:
                    long = (i, candle)
                    break
        elif candle['Supertrend_Signal']==-1:
            if long:
                trades.append({"type": "long", "id": long[0], "profit": candle['Close']>long[1]['Close']})
                long=None
            for x in data[i-margin : i+1]:
                if x['MACD_Signal'] == -1 and x['MACD']>0:
                    short = (i, candle)
                    break

        if candle['MACD_Signal']==1 and candle['MACD']<0:
            for x in data[i-margin : i+1]:
                if x['Supertrend_Signal'] == 1:
                    long = (i, candle)
                    break
        elif candle['MACD_Signal']==-1 and candle['MACD']>0:
            for x in data[i-margin : i+1]:
                if x['Supertrend_Signal'] == -1:
                    short = (i, candle)
                    break

    if len(trades)==0:
        return 0, 0
    
    profitPercent = 0
    for i in trades:
        if i['profit']:
            profitPercent+=1
    return len(trades), profitPercent









