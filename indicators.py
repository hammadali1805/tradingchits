import yfinance as yf
import pandas_ta as ta
import pandas as pd
import numpy as np

def fetch_and_calculate_indicators(ticker, period="1y", interval="1d"):
    # Fetch data from yfinance
    df = yf.download(ticker, period=period, interval=interval)
    
    # Drop rows with missing values
    df.dropna(inplace=True)

    # 0-9
    # 1. 52 Week High/Low
    df['52_Week_High'] = df['High'].rolling(window=252).max()
    df['52_Week_Low'] = df['Low'].rolling(window=252).min()

    # A
    # 2. Accelerator Oscillator
    df['AO'] = ta.ao(df['High'], df['Low'])
    
    # 3. Accumulation/Distribution
    df['AD'] = ta.ad(df['High'], df['Low'], df['Close'], df['Volume'])
    
    # 4. Accumulative Swing Index
    # df['ASI'] = ta.asi(df['Open'], df['High'], df['Low'], df['Close'])
    
    # 5. Advance/Decline
    df['Advance_Decline'] = df['Close'].diff()
    
    # 6. Arnaud Legoux Moving Average
    df['ALMA'] = ta.alma(df['Close'])
    
    # 7. Aroon
    # df['AROON'] = ta.aroon(df['Close'])
    
    # 8. Average Directional Index
    # df['ADX'] = ta.adx(df['High'], df['Low'], df['Close'])
    
    # 9. Average Price
    df['Average_Price'] = (df['High'] + df['Low'] + df['Close']) / 3
    
    # 10. Average True Range
    df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'])
    
    # 11. Awesome Oscillator
    df['Awesome_Oscillator'] = ta.ao(df['High'], df['Low'])
    
    # B
    # 12. Balance of Power
    df['BOP'] = ta.bop(df['Open'], df['High'], df['Low'], df['Close'])
    
    # 13. Bollinger Bands
    # df['Bollinger_Bands'] = ta.bbands(df['Close'])
    
    # 14. Bollinger Bands %B
    # df['Bollinger_Bands_%B'] = ta.bbands(df['Close'], mamode='sma')['BBP_20_2.0']
    
    # 15. Bollinger Bands Width
    # df['Bollinger_Bands_Width'] = df['Bollinger_Bands']['BBU_20_2.0'] - df['Bollinger_Bands']['BBL_20_2.0']
    
    # C
    # 16. Chaikin Money Flow
    df['CMF'] = ta.cmf(df['High'], df['Low'], df['Close'], df['Volume'])
    
    # 17. Chaikin Oscillator
    df['Chaikin_Oscillator'] = ta.adosc(df['High'], df['Low'], df['Close'], df['Volume'])
    
    # 18. Chaikin Volatility
    # df['Chaikin_Volatility'] = ta.chaikin(df['High'], df['Low'], df['Close'])
    
    # 19. Chande Kroll Stop
    # df['CKS'] = ta.cksp(df['High'], df['Low'], df['Close'])
    
    # 20. Chande Momentum Oscillator
    df['CMO'] = ta.cmo(df['Close'])
    
    # 21. Chop Zone
    df['Chop_Zone'] = ta.chop(df['High'], df['Low'], df['Close'])
    
    # 22. Choppiness Index
    df['Choppiness_Index'] = ta.chop(df['High'], df['Low'], df['Close'])
    
    # 23. Commodity Channel Index
    df['CCI'] = ta.cci(df['High'], df['Low'], df['Close'])
    
    # 24. Connors RSI
    df['Connors_RSI'] = ta.rsi(df['Close'])
    
    # 25. Coppock Curve
    df['Coppock_Curve'] = ta.coppock(df['Close'])
    
    # 26. Correlation Coefficient
    df['Correlation_Coefficient'] = df['Close'].rolling(window=20).corr(df['Close'].shift())
    
    # 27. Correlation - Log
    df['Correlation_Log'] = df['Close'].rolling(window=20).corr(df['Close'].apply(np.log).shift())
    
    # D
    # 28. Detrended Price Oscillator
    df['DPO'] = ta.dpo(df['Close'])
    
    # 29. Directional Movement
    # df['Directional_Movement'] = ta.dm(df['High'], df['Low'], df['Close'])
    
    # 30. Donchian Channels
    # df['Donchian_Channels'] = ta.donchian(df['High'], df['Low'], df['Close'])
    
    # 31. Double EMA
    df['Double_EMA'] = ta.dema(df['Close'])
    
    # E
    # 32. Ease of Movement
    df['EOM'] = ta.eom(df['High'], df['Low'], df['Close'], df['Volume'])
    
    # 33. Elder's Force Index
    df['EFI'] = ta.efi(df['Close'], df['Volume'])
    
    # 34. EMA Cross
    df['EMA_Cross'] = ta.ema(df['Close'], 12) - ta.ema(df['Close'], 26)
    
    # 35. Envelopes
    df['Envelopes'] = ta.ema(df['Close'], 20)
    
    # F
    # 36. Fisher Transform
    # df['Fisher_Transform'] = ta.fisher(df['High'], df['Low'])
    
    # G
    # 37. Guppy Multiple Moving Average
    # df['Guppy_MMA'] = ta.gmma(df['Close'])
    
    # H
    # 38. Historical Volatility
    # df['Historical_Volatility'] = ta.hv(df['Close'])
    
    # 39. Hull Moving Average
    df['HMA'] = ta.hma(df['Close'])
    
    # I
    # 40. Ichimoku Cloud
    # df['Ichimoku_Cloud'] = ta.ichimoku(df['High'], df['Low'], df['Close'])
    
    # K
    # 41. Keltner Channels
    # df['Keltner_Channels'] = ta.kc(df['High'], df['Low'], df['Close'])
    
    # 42. Klinger Oscillator
    # df['Klinger_Oscillator'] = ta.kvo(df['High'], df['Low'], df['Close'], df['Volume'])
    
    # 43. Know Sure Thing
    # df['KST'] = ta.kst(df['Close'])
    
    # L
    # 44. Least Squares Moving Average
    # df['LSMA'] = ta.lsma(df['Close'])
    
    # 45. Linear Regression Curve
    df['Linear_Regression_Curve'] = ta.linreg(df['Close'])
    
    # 46. Linear Regression Slope
    df['Linear_Regression_Slope'] = ta.linreg(df['Close'])
    
    # M
    # 47. MA Cross
    df['MA_Cross'] = ta.sma(df['Close'], 10) - ta.sma(df['Close'], 20)
    
    # 48. MA with EMA Cross
    df['MA_EMA_Cross'] = ta.sma(df['Close'], 10) - ta.ema(df['Close'], 20)
    
    # 49. Mass Index
    df['Mass_Index'] = ta.massi(df['High'], df['Low'])
    
    # 50. McGinley Dynamic
    # df['McGinley_Dynamic'] = ta.mcdx(df['Close'])
    
    # 51. Median Price
    df['Median_Price'] = (df['High'] + df['Low']) / 2
    
    # 52. Momentum
    df['Momentum'] = ta.mom(df['Close'])
    
    # 53. Money Flow Index
    df['MFI'] = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'])
    
    # 54. Moving Average
    df['Moving_Average'] = ta.sma(df['Close'], 20)
    
    # 55. Moving Average Channel
    df['Moving_Average_Channel'] = ta.sma(df['Close'], 20)
    
    # 56. MACD
    # df['MACD'] = ta.macd(df['Close'])
    
    # 57. Moving Average Exponential
    df['EMA'] = ta.ema(df['Close'])
    
    # 58. Moving Average Weighted
    df['WMA'] = ta.wma(df['Close'])
    
    # 59. Moving Average Double
    df['Double_MA'] = ta.dema(df['Close'])
    
    # 60. Moving Average Triple
    df['Triple_MA'] = ta.tema(df['Close'])
    
    # 61. Moving Average Adaptive
    df['Adaptive_MA'] = ta.kama(df['Close'])
    
    # 62. Moving Average Hamming
    df['Hamming_MA'] = ta.wma(df['Close'])
    
    # 63. Moving Average Multiple
    df['Multiple_MA'] = ta.sma(df['Close'])
    
    # 64. Majority Rule
    df['Majority_Rule'] = ta.sma(df['Close'])
    
    # N
    # 65. Net Volume
    df['Net_Volume'] = df['Volume'] - df['Volume'].shift()
    
    # O
    # 66. On Balance Volume
    df['OBV'] = ta.obv(df['Close'], df['Volume'])
    
    # P
    # 67. Parabolic SAR
    # df['Parabolic_SAR'] = ta.psar(df['High'], df['Low'], df['Close'])
    
    # 68. Pivot Points Standard
    # df['Pivot_Points'] = ta.pivot(df['High'], df['Low'], df['Close'])
    
    # 69. Price Channel
    # df['Price_Channel'] = ta.donchian(df['High'], df['Low'], df['Close'])
    
    # 70. Price Oscillator
    df['Price_Oscillator'] = ta.pgo(df['High'], df['Low'], df['Close'])
    
    # 71. Price Volume Trend
    df['PVT'] = ta.pvt(df['Close'], df['Volume'])
    
    # R
    # 72. Rate Of Change
    df['ROC'] = ta.roc(df['Close'])
    
    # 73. Ratio
    df['Ratio'] = df['Close'] / df['Close'].shift()
    
    # 74. Relative Strength Index
    df['RSI'] = ta.rsi(df['Close'])
    
    # 75. Relative Vigor Index
    df['RVI'] = ta.rvi(df['Close'])
    
    # 76. Relative Volatility Index
    df['RVI'] = ta.rvi(df['Close'])
    
    # S
    # 77. Standard Error
    df['Standard_Error'] = df['Close'].rolling(window=20).std()
    
    # 78. Standard Error Bands
    # df['SE_Bands'] = ta.bbands(df['Close'])
    
    # 79. SMI Ergodic Indicator/Oscillator
    # df['SMI'] = ta.smi(df['Close'])
    
    # 80. Smoothed Moving Average
    df['Smoothed_MA'] = ta.sma(df['Close'], 10)
    
    # 81. Standard Deviation
    df['Standard_Deviation'] = ta.stdev(df['Close'])
    
    # 82. Stochastic
    # df['Stochastic'] = ta.stoch(df['High'], df['Low'], df['Close'])
    
    # 83. Stochastic RSI
    # df['Stochastic_RSI'] = ta.stochrsi(df['Close'])
    
    # 84. SuperTrend
    # df['SuperTrend'] = ta.supertrend(df['High'], df['Low'], df['Close'])
    
    # 85. Spread
    df['Spread'] = df['High'] - df['Low']
    
    # T
    # 86. TRIX
    # df['TRIX'] = ta.trix(df['Close'])
    
    # 87. Triple EMA
    df['Triple_EMA'] = ta.tema(df['Close'])
    
    # 88. True Strength Indicator
    # df['TSI'] = ta.tsi(df['Close'])
    
    # 89. Trend Strength Index
    # df['TSI'] = ta.tsi(df['Close'])
    
    # 90. Typical Price
    df['Typical_Price'] = (df['High'] + df['Low'] + df['Close']) / 3
    
    # U
    # 91. Ultimate Oscillator
    df['Ultimate_Oscillator'] = ta.uo(df['High'], df['Low'], df['Close'])
    
    # V
    # 92. Volatility Close-to-Close
    df['Volatility_CtC'] = df['Close'].rolling(window=20).std()
    
    # 93. Volatility Zero Trend Close-to-Close
    df['Volatility_ZT'] = df['Close'].rolling(window=20).std()
    
    # 94. Volatility O-H-L-C
    df['Volatility_OHLC'] = ta.stdev(df['Close'])
    
    # 95. Volatility Index
    df['Volatility_Index'] = df['Close'].rolling(window=20).std()
    
    # 96. VWAP
    df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'])
    
    # 97. VWMA
    df['VWMA'] = ta.vwma(df['Close'], df['Volume'])
    
    # 98. Volume Oscillator
    df['Volume_Oscillator'] = df['Volume'].rolling(window=20).mean()
    
    # 99. Volume Profile Fixed Range
    df['Volume_Profile_FR'] = df['Volume']
    
    # 100. Volume Profile Visible Range
    df['Volume_Profile_VR'] = df['Volume']
    
    # 101. Vortex Indicator
    # df['Vortex_Indicator'] = ta.vortex(df['High'], df['Low'], df['Close'])
    
    # 102. Volume
    df['Volume'] = df['Volume']
    
    # W
    # 103. Williams %R
    df['Williams_%R'] = ta.willr(df['High'], df['Low'], df['Close'])
    
    # 104. Williams Alligator
    # df['Williams_Alligator'] = ta.alligator(df['High'], df['Low'], df['Close'])
    
    # 105. Williams Fractal
    # df['Williams_Fractal'] = ta.fractal(df['High'], df['Low'], df['Close'])
    
    # Z
    # 106. ZigZag
    # df['ZigZag'] = ta.zigzag(df['High'], df['Low'], df['Close'])

    return df

# Example usage
ticker = "AAPL"
df = fetch_and_calculate_indicators(ticker)

# Display the first few rows of the dataframe
print(df.head())