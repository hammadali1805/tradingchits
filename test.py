import yfinance as yf
import pandas as pd
import pandas_ta as ta
import math

# # Define the ticker and the date range
# ticker = "AAPL"
# start_date = "2022-01-01"
# end_date = "2023-01-01"

# # Fetch the data
# data = yf.download(ticker, start=start_date, end=end_date)

data = pd.read_csv("aapl_2023.csv")

# Initialize the DataFrame for insights and signals
insights_signals_df = pd.DataFrame(index=data.index)

# 1. 52 Week High/Low
data['52_Week_High'] = data['High'].rolling(window=252).max()
data['52_Week_Low'] = data['Low'].rolling(window=252).min()
insights_signals_df['52_Week_Insight'] = ['Strong bullish sentiment' if close > high else 'Strong bearish sentiment' if close < low else None  for close, high, low in zip(data['Close'], data['52_Week_High'], data['52_Week_Low'])]
f2week_signal = [None]
for i in range(1, len(data)):
    if data['Close'].iloc[i] > data['52_Week_High'].iloc[i] and data['Close'].iloc[i-1] <= data['52_Week_High'].iloc[i-1]:
        f2week_signal.append('Buy')
    elif data['Close'].iloc[i] < data['52_Week_Low'].iloc[i] and data['Close'].iloc[i-1] >= data['52_Week_Low'].iloc[i-1]:
        f2week_signal.append('Sell')
    else:
        f2week_signal.append(None)
insights_signals_df['52_Week_Signal'] = f2week_signal

# 2. Accelerator Oscillator (Not directly available in pandas_ta)
# Custom calculation for Accelerator Oscillator
data['AO'] = ta.ao(data['High'], data['Low'])
data['AC'] = data['AO'] - data['AO'].rolling(window=5).mean()
insights_signals_df['AC_Insight'] = ['Bullish trend' if ac > 0 else 'Bearish trend' for ac in data['AC']]
ac_signal = [None]
for i in range(1, len(data)):
    if data['AC'].iloc[i] > 0 and data['AC'].iloc[i-1] <= 0:
        ac_signal.append('Buy')
    elif data['AC'].iloc[i] < 0 and data['AC'].iloc[i-1] >= 0:
        ac_signal.append('Sell')
    else:
        ac_signal.append(None)
insights_signals_df['AC_Signal'] = ac_signal

# 3. Accumulation/Distribution
data['AD'] = ta.ad(data['High'], data['Low'], data['Close'], data['Volume'])
data['AD_Shifted'] = data['AD'].shift(1)
insights_signals_df['AD_Insight'] = ['Accumulation' if ad > ad_shifted else 'Distribution' for ad, ad_shifted in zip(data['AD'], data['AD_Shifted'])]
insights_signals_df['AD_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 4. Accumulative Swing Index (Not directly available in pandas_ta)
# Custom calculation for Accumulative Swing Index
# Placeholder as the calculation is complex and needs further context
insights_signals_df['ASI_Insight'] = [None] * len(data)
insights_signals_df['ASI_Signal'] = [None] * len(data)

# 5. Advance/Decline (Not directly available in pandas_ta)
# Custom calculation for Advance/Decline Line
# Placeholder as this typically requires market-wide data
insights_signals_df['ADL_Insight'] = [None] * len(data)
insights_signals_df['ADL_Signal'] = [None] * len(data)

# 6. Arnaud Legoux Moving Average
data['ALMA'] = ta.alma(data['Close'])
insights_signals_df['ALMA_Insight'] = ['Bullish trend' if close > alma else 'Bearish trend' for close, alma in zip(data['Close'], data['ALMA'])]
alma_signal = [None]
for i in range(1, len(data)):
    if data['Close'].iloc[i] > data['ALMA'].iloc[i] and data['Close'].iloc[i-1] <= data['ALMA'].iloc[i-1]:
        alma_signal.append('Buy')
    elif data['Close'].iloc[i] < data['ALMA'].iloc[i] and data['Close'].iloc[i-1] >= data['ALMA'].iloc[i-1]:
        alma_signal.append('Sell')
    else:
        alma_signal.append(None)
insights_signals_df['ALMA_Signal'] = alma_signal

# 7. Aroon
aroon = ta.aroon(data['High'], data['Low'], length=25)
data['Aroon_Up'] = aroon['AROOND_25']
data['Aroon_Down'] = aroon['AROONU_25']
insights_signals_df['Aroon_Insight'] = ['Strong uptrend' if up > 70 else 'Strong downtrend' if down > 70 else None for up, down in zip(data['Aroon_Up'], data['Aroon_Down'])]
aroon_signal = [None]
for i in range(1, len(data)):
    if data['Aroon_Up'].iloc[i] > data['Aroon_Down'].iloc[i] and data['Aroon_Up'].iloc[i-1] <= data['Aroon_Down'].iloc[i-1]:
        aroon_signal.append('Buy')
    elif data['Aroon_Down'].iloc[i] > data['Aroon_Up'].iloc[i] and data['Aroon_Down'].iloc[i-1] <= data['Aroon_Up'].iloc[i-1]:
        aroon_signal.append('Sell')
    else:
        aroon_signal.append(None)
insights_signals_df['Aroon_Signal'] = aroon_signal

# 8. Average Directional Index
adx = ta.adx(data['High'], data['Low'], data['Close'])
data['ADX'] = adx['ADX_14']
insights_signals_df['ADX_Insight'] = ['Strong trend' if adx > 25 else 'Weak trend' if adx < 20 else None for adx in data['ADX']]
adx_signal = [None]
for i in range(1, len(data)):
    if adx['DMP_14'].iloc[i] > adx['DMN_14'].iloc[i] and adx['DMP_14'].iloc[i-1] <= adx['DMN_14'].iloc[i-1]:
        adx_signal.append('Buy')
    elif adx['DMN_14'].iloc[i] > adx['DMP_14'].iloc[i] and adx['DMN_14'].iloc[i-1] <= adx['DMP_14'].iloc[i-1]:
        adx_signal.append('Sell')
    else:
        adx_signal.append(None)
insights_signals_df['ADX_Signal'] = adx_signal

# 9. Average Price
data['Avg_Price'] = (data['High'] + data['Low']) / 2
insights_signals_df['Avg_Price_Insight'] = [None] * len(data) #No specific insight
insights_signals_df['Avg_Price_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 10. Average True Range
data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'])
atr_mean = data['ATR'].mean()
insights_signals_df['ATR_Insight'] = ['High volatility' if atr > atr_mean else 'Low volatility' for atr in data['ATR']]
insights_signals_df['ATR_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 11. Awesome Oscillator
data['AO'] = ta.ao(data['High'], data['Low'])
insights_signals_df['AO_Insight'] = ['Bullish momentum' if ao > 0 else 'Bearish momentum' if ao < 0 else None for ao in data['AO']]
ao_signal = [None]
for i in range(1, len(data)):
    if data['AO'].iloc[i] > 0 and data['AO'].iloc[i-1] <= 0:
        ao_signal.append('Buy')
    elif data['AO'].iloc[i] < 0 and data['AO'].iloc[i-1] >= 0:
        ao_signal.append('Sell')
    else:
        ao_signal.append(None)
insights_signals_df['AO_Signal'] = ao_signal

# 12. Balance of Power
data['BOP'] = ta.bop(data['Open'], data['High'], data['Low'], data['Close'])
insights_signals_df['BOP_Insight'] = ['Buying pressure' if bop > 0 else 'Selling pressure' if bop < 0 else None for bop in data['BOP']]
insights_signals_df['BOP_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 13. Bollinger Bands
bb = ta.bbands(data['Close'])
data['BB_Upper'] = bb['BBU_5_2.0']
data['BB_Middle'] = bb['BBM_5_2.0']
data['BB_Lower'] = bb['BBL_5_2.0']
insights_signals_df['BB_Insight'] = ['Overbought' if close >= upper*0.95 else 'Oversold' if close <= lower*1.05 else None for close, upper, lower in zip(data['Close'], data['BB_Upper'], data['BB_Lower'])]
bb_signal = [None]
for i in range(1, len(data)):
    if data['High'].iloc[i] >= data['BB_Upper'].iloc[i] and data['High'].iloc[i-1] < data['BB_Upper'].iloc[i-1]:
        bb_signal.append('Sell')
    elif data['Low'].iloc[i] <= data['BB_Lower'].iloc[i] and data['Low'].iloc[i-1] > data['BB_Lower'].iloc[i-1]:
        bb_signal.append('Buy')
    else:
        bb_signal.append(None)
insights_signals_df['BB_Signal'] = bb_signal

# 14. Bollinger Bands %B
data['BB_%B'] = (data['Close'] - data['BB_Lower']) / (data['BB_Upper'] - data['BB_Lower'])
insights_signals_df['BB_%B_Insight'] = ['Overbought' if bbp > 1 else 'Oversold' if bbp < 0 else None for bbp in data['BB_%B']]
bbp_signal = [None]
for i in range(1, len(data)):
    if data['BB_%B'].iloc[i] > 1 and data['BB_%B'].iloc[i-1] <= 1:
        bbp_signal.append('Sell')
    elif data['BB_%B'].iloc[i] < 0 and data['BB_%B'].iloc[i-1] >= 0:
        bbp_signal.append('Buy')
    else:
        bbp_signal.append(None)
insights_signals_df['BB_%B_Signal'] = bbp_signal

# 15. Bollinger Bands Width
data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / data['BB_Middle']
bb_width_mean = data['BB_Width'].mean()
insights_signals_df['BB_Width_Insight'] = ['High volatility' if width > bb_width_mean else 'Low volatility' for width in data['BB_Width']]
insights_signals_df['BB_Width_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 16. Chaikin Money Flow
data['CMF'] = ta.cmf(data['High'], data['Low'], data['Close'], data['Volume'])
insights_signals_df['CMF_Insight'] = ['Buying pressure' if cmf > 0 else 'Selling pressure' if cmf < 0 else None for cmf in data['CMF']]
insights_signals_df['CMF_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 17. Chaikin Oscillator
data['AD'] = ta.ad(data['High'], data['Low'], data['Close'], data['Volume'])
data['AD_EMA_3'] = ta.ema(data['AD'], length=3)
data['AD_EMA_10'] = ta.ema(data['AD'], length=10)
data['Chaikin_Oscillator'] = data['AD_EMA_3'] - data['AD_EMA_10']
insights_signals_df['Chaikin_Osc_Insight'] = ['Buying pressure' if co > 0 else 'Selling Pressure' if co < 0 else None for co in data['Chaikin_Oscillator']]
insights_signals_df['Chaikin_Osc_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 18. Chaikin Volatility
data['Chaikin_Volatility'] = ta.roc(ta.ema(data['High'] - data['Low'], length=10), length=10)
insights_signals_df['Chaikin_Vol_Insight'] = ['High volatility' if cv > 50 else 'Low volatility' if cv < -50 else None for cv in data['Chaikin_Volatility']]
insights_signals_df['Chaikin_Vol_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 19. Chande Kroll Stop (Not directly available in pandas_ta)
# Placeholder as the calculation is complex and needs further context
insights_signals_df['CKS_Insight'] = [None] * len(data)
insights_signals_df['CKS_Signal'] = [None] * len(data)

# 20. Chande Momentum Oscillator
data['CMO'] = ta.cmo(data['Close'])
insights_signals_df['CMO_Insight'] = ['Overbought' if cmo > 50 else 'Oversold' if cmo < -50 else None for cmo in data['CMO']]
cmo_signal = [None]
for i in range(1, len(data)):
    if data['CMO'].iloc[i] > 50 and data['CMO'].iloc[i-1] <= 50:
        cmo_signal.append('Sell')
    elif data['CMO'].iloc[i] < -50 and data['CMO'].iloc[i-1] >= -50:
        cmo_signal.append('Buy')
    else:
        cmo_signal.append(None)
insights_signals_df['CMO_Signal'] = cmo_signal

# 21. Chop Zone (Placeholder due to library limitations)
insights_signals_df['CZ_Insight'] = [None] * len(data)
insights_signals_df['CZ_Signal'] = [None] * len(data)

# 22. Choppiness Index
data['CHOP'] = ta.chop(data['High'], data['Low'], data['Close'])
chop_mean = data['CHOP'].mean()
insights_signals_df['CHOP_Insight'] = ['Choppy market' if chop > chop_mean else 'Trending market' for chop in data['CHOP']]
insights_signals_df['CHOP_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 23. Commodity Channel Index
data['CCI'] = ta.cci(data['High'], data['Low'], data['Close'])
insights_signals_df['CCI_Insight'] = ['Overbought' if cci > 100 else 'Oversold' if cci < -100 else None for cci in data['CCI']]
insights_signals_df['CCI_Signal'] = ['Buy' if cci < -100 and prev_cci >= -100 else 'Sell' if cci > 100 and prev_cci <= 100 else None for cci, prev_cci in zip(data['CCI'], data['CCI'].shift(1))]

# 24. Connors RSI
insights_signals_df['CRSI_Insight'] = [None] * len(data)
insights_signals_df['CRSI_Signal'] = [None] * len(data)

# 25. Coppock Curve
data['CC'] = ta.coppock(data['Close'])
insights_signals_df['CC_Insight'] = ['Bullish trend' if cc > 0 else 'Bearish trend' for cc in data['CC']]
insights_signals_df['CC_Signal'] = ['Buy' if cc > 0 and prev_cc <= 0 else 'Sell' if cc < 0 and prev_cc >= 0 else None for cc, prev_cc in zip(data['CC'], data['CC'].shift(1))]

# 26. Correlation Coefficient (Placeholder due to complexity)
insights_signals_df['CCo_Insight'] = [None] * len(data)
insights_signals_df['CCo_Signal'] = [None] * len(data)

# 27. Correlation - Log (Placeholder due to complexity)
insights_signals_df['CLog_Insight'] = [None] * len(data)
insights_signals_df['CLog_Signal'] = [None] * len(data)

# 28. Detrended Price Oscillator
data['DPO'] = ta.dpo(data['Close'])
insights_signals_df['DPO_Insight'] = ['Bullish momentum' if dpo > 0 else 'Bearish momentum' for dpo in data['DPO']]
insights_signals_df['DPO_Signal'] = ['Buy' if dpo > 0 and prev_dpo <= 0 else 'Sell' if dpo < 0 and prev_dpo >= 0 else None for dpo, prev_dpo in zip(data['DPO'], data['DPO'].shift(1))]

# 29. Directional Movement Index (DMI) - Breaking it down
adx = ta.adx(data['High'], data['Low'], data['Close'])
data['DMI_Plus'] = adx['DMP_14']
data['DMI_Minus'] = adx['DMN_14']
data['DMI_ADX'] = adx['ADX_14']
insights_signals_df['DMI_Insight'] = ['Bullish trend' if dmiplus > dmiminus else 'Bearish trend' for dmiplus, dmiminus in zip(data['DMI_Plus'], data['DMI_Minus'])]
insights_signals_df['DMI_Signal'] = ['Buy' if dmiplus > dmiminus and prev_dmiplus <= prev_dmiminus else 'Sell' if dmiplus < dmiminus and prev_dmiplus >= prev_dmiminus else None for dmiplus, dmiminus, prev_dmiplus, prev_dmiminus in zip(data['DMI_Plus'], data['DMI_Minus'], data['DMI_Plus'].shift(1), data['DMI_Minus'].shift(1))]

# 30. Donchian Channels
donchian = ta.donchian(data['High'], data['Low'], upper_length=20, lower_length=20)
data['Donchian_Upper'] = donchian['DCU_20_20']
data['Donchian_Lower'] = donchian['DCL_20_20']
insights_signals_df['Donchian_Insight'] = ['Bullish trend' if close > donchian_upper else 'Bearish trend' if close < donchian_lower else None for close, donchian_upper, donchian_lower in zip(data['Close'], data['Donchian_Upper'], data['Donchian_Lower'])]
insights_signals_df['Donchian_Signal'] = ['Buy' if close > donchian_upper and prev_close <= prev_donchian_upper else 'Sell' if close < donchian_lower and prev_close >= prev_donchian_lower else None for close, prev_close, donchian_upper, donchian_lower, prev_donchian_upper, prev_donchian_lower in zip(data['Close'], data['Close'].shift(1), data['Donchian_Upper'], data['Donchian_Lower'], data['Donchian_Upper'].shift(1), data['Donchian_Lower'].shift(1))]

# 31. Double EMA
data['DEMA'] = ta.dema(data['Close'])
insights_signals_df['DEMA_Insight'] = ['Bullish trend' if close > dema else 'Bearish trend' if close < dema else None for close, dema in zip(data['Close'], data['DEMA'])]
insights_signals_df['DEMA_Signal'] = ['Buy' if close > dema and prev_close <= prev_dema else 'Sell' if close < dema and prev_close >= prev_dema else None for close, prev_close, dema, prev_dema in zip(data['Close'], data['Close'].shift(1), data['DEMA'], data['DEMA'].shift(1))]

# 32. Ease of Movement
data['EMV'] = ta.eom(data['High'], data['Low'], data['Close'], data['Volume'])
insights_signals_df['EMV_Insight'] = ['Price easily moves upward' if emv > 0 else 'Price easily moves downward' for emv in data['EMV']]
insights_signals_df['EMV_Signal'] = [None] * len(data)  # No specific buy/sell signal

# 33. Elder's Force Index
data['EFI'] = ta.efi(data['Close'], data['Volume'])
insights_signals_df['EFI_Insight'] = ['Bullish terend' if efi > 0 else 'Bearish trend' if efi < 0 else None for efi in data['EFI']]
insights_signals_df['EFI_Signal'] = ['Buy' if efi > 0 and prev_efi <= 0 else 'Sell' if efi < 0 and prev_efi >= 0 else None for efi, prev_efi in zip(data['EFI'], data['EFI'].shift(1))]

# 34. EMA Cross
ema9 = ta.ema(data['Close'], length=9)
ema21 = ta.ema(data['Close'], length=21)
data['EMA9'] = ema9
data['EMA21'] = ema21
insights_signals_df['EMA_Cross_Insight'] = ['Bullish trend' if short_ema > long_ema else 'Bearish trend' for short_ema, long_ema in zip(ema9, ema21)]
insights_signals_df['EMA_Cross_Signal'] = ['Buy' if e1 > e2 and prev_e1 <= prev_e2 else 'Sell' if e1 < e2 and prev_e1 >= prev_e2 else None for e1, e2, prev_e1, prev_e2 in zip(data['EMA9'], data['EMA21'], data['EMA9'].shift(1), data['EMA21'].shift(1))]

# 35. Envelopes (Manually calculated)
sma = ta.sma(data['Close'], length=20)
data['Envelope_Upper'] = sma * 1.02
data['Envelope_Lower'] = sma * 0.98
insights_signals_df['Envelope_Insight'] = ['Overbought' if close > env_upper else 'Oversold' if close < env_lower else None for close, env_upper, env_lower in zip(data['Close'], data['Envelope_Upper'], data['Envelope_Lower'])]
insights_signals_df['Envelope_Signal'] = ['Sell' if close > env_upper and prev_close <= prev_env_upper else 'Buy' if close < env_lower and prev_close >= prev_env_lower else None for close, prev_close, env_upper, env_lower, prev_env_upper, prev_env_lower in zip(data['Close'], data['Close'].shift(1), data['Envelope_Upper'], data['Envelope_Lower'], data['Envelope_Upper'].shift(1), data['Envelope_Lower'].shift(1))]

# 36. Fisher Transform
fisher = ta.fisher(data['High'], data['Low'])
data['Fisher'] = fisher['FISHERT_9_1']
data['Fisher_Signal'] = fisher['FISHERTs_9_1']
insights_signals_df['Fisher_Insight'] = ['Bullish trend' if fisher > 0 else 'Bearish trend' if fisher < 0 else None for fisher in data['Fisher']]
insights_signals_df['Fisher_Signal'] = ['Buy' if fisher > 0 and prev_fisher <= 0 else 'Sell' if fisher < 0 and prev_fisher >= 0 else None for fisher, prev_fisher in zip(data['Fisher'], data['Fisher'].shift(1))]

# 37. Guppy Multiple Moving Average (GMMA)
insights_signals_df['GMMA_Insight'] = [None] * len(data)
insights_signals_df['GMMA_Signal'] = [None] * len(data)

# 38. Historical Volatility
data['c/c1'] = [math.log(c/c1) for c, c1 in zip(data['Close'], data['Close'].shift(1))]
data['Historical_Volatility'] = 100 * ta.stdev(data['c/c1'], 10) * math.sqrt(365 / 1) #1 is for daily
hv_mean = data['Historical_Volatility'].mean()
insights_signals_df['HV_Insight'] = ['High volatility' if hv > hv_mean else 'Low volatility'  for hv in data['Historical_Volatility']]
insights_signals_df['HV_Signal'] = [None] * len(data)

# 39. Hull Moving Average
data['HMA'] = ta.hma(data['Close'])
insights_signals_df['HMA_Insight'] = ['Bullish trend' if close > hma else 'Bearish trend' for close, hma in zip(data['Close'], data['HMA'])]
insights_signals_df['HMA_Signal'] = ['Buy' if close > hma and prev_close <= prev_hma else 'Sell' if close < hma and prev_close >= prev_hma else None for close, hma, prev_close, prev_hma in zip(data['Close'], data['HMA'], data['Close'].shift(1), data['HMA'].shift(1))]

# 40. Ichimoku Cloud
ichimoku = ta.ichimoku(data['High'], data['Low'], data['Close'])[0]
data['Ichimoku_Conversion'] = ichimoku['ITS_9']
data['Ichimoku_Base'] = ichimoku['IKS_26']
data['Ichimoku_Lagging'] = ichimoku['ICS_26']
data['Ichimoku_Leading_A'] = ichimoku['ISA_9']
data['Ichimoku_Leading_B'] = ichimoku['ISB_26']
data['Cloud'] = [a if a>b else b  for a, b in zip(data['Ichimoku_Leading_A'], data['Ichimoku_Leading_B'])]
insights_signals_df['Ichimoku_Insight'] = ['Bullish trend' if close > cloud else 'Bearish trend' for close, cloud in zip(data['Close'],data['Cloud'])]
insights_signals_df['Ichimoku_Signal'] = ['Buy' if conv > base and prev_conv <= prev_base else 'Sell' if conv < base and prev_conv >= prev_base else None for conv, base, prev_conv, prev_base in zip(data['Ichimoku_Conversion'], data['Ichimoku_Base'], data['Ichimoku_Conversion'].shift(1), data['Ichimoku_Base'].shift(1))]

# 41. Keltner Channels
kc = ta.kc(data['High'], data['Low'], data['Close'])
data['KC_Upper'] = kc['KCUe_20_2']
data['KC_Lower'] = kc['KCLe_20_2']
insights_signals_df['KC_Insight'] = ['Bullish trend' if close > upper else 'Bearish trend' if close < lower else None for close, upper, lower in zip(data['Close'], data['KC_Upper'], data['KC_Lower'])]
insights_signals_df['KC_Signal'] = ['Buy' if close > upper and prev_close <= prev_upper else 'Sell' if close < lower and prev_close >= prev_lower else None for close, upper, lower, prev_close, prev_upper, prev_lower in zip(data['Close'], data['KC_Upper'], data['KC_Lower'], data['Close'].shift(1), data['KC_Upper'].shift(1), data['KC_Lower'].shift(1))]

# 42. Klinger Oscillator
insights_signals_df['KO_Insight'] = [None] * len(data)
insights_signals_df['KO_Signal'] = [None] * len(data)

# 43. Know Sure Thing (KST)
kst = ta.kst(data['Close'])
data['KST'] = kst['KST_10_15_20_30_10_10_10_15']
data['KST_Signal'] = kst['KSTs_9']
insights_signals_df['KST_Insight'] = ['Bullish' if kst_val > kst_signal else 'Bearish' for kst_val, kst_signal in zip(data['KST'], data['KST_Signal'])]
insights_signals_df['KST_Signal'] = ['Buy' if kst_val > kst_signal and prev_kst_val <= prev_kst_signal else 'Sell' if kst_val < kst_signal and prev_kst_val >= prev_kst_signal else None for kst_val, kst_signal, prev_kst_val, prev_kst_signal in zip(data['KST'], data['KST_Signal'], data['KST'].shift(1), data['KST_Signal'].shift(1))]

# 44. Least Squares Moving Average
data['LSMA'] = ta.linreg(data['Close'])
insights_signals_df['LSMA_Insight'] = ['Bullish trend' if close > lsma else 'Bearish trend' for close, lsma in zip(data['Close'], data['LSMA'])]
insights_signals_df['LSMA_Signal'] = ['Buy' if close > lsma and prev_close <= prev_lsma else 'Sell' if close < lsma and prev_close >= prev_lsma else None for close, lsma, prev_close, prev_lsma in zip(data['Close'], data['LSMA'], data['Close'].shift(1), data['LSMA'].shift(1))]

# 45. Linear Regression Curve
insights_signals_df['Linear_Regression_Curve_Insight'] = [None] * len(data)
insights_signals_df['Linear_Regression_Curve_Signal'] = [None] * len(data)

# 46. Linear Regression Slope
insights_signals_df['Linear_Regression_Slope_Insight'] = [None] * len(data)
insights_signals_df['Linear_Regression_Slope_Signal'] = [None] * len(data)

data.to_csv('aapl_2023_processed.csv')

# Fill NaN values
insights_signals_df.fillna(method='bfill', inplace=True)

# Display the first few rows
print(insights_signals_df.head())
