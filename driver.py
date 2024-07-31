from strategy import strategy
import pandas as pd

symbols = [
    # Cryptocurrencies
    "BTC-USD",  # Bitcoin
]

intervals = [
    ("15m", "1mo", 3, 14),  # 15 minutes
]

data = []
for symbol in symbols:
    for interval, period, a, m in intervals:
        for margin in [3,]:
            no_of_trades, profit_percent  = strategy(symbol=symbol, interval=interval, period=period, atr_period=a, multiplier=m, margin=margin)
            record = {
                "Symbol": symbol,
                "Interval": interval,
                "Period": period,
                "Atr_Period": a,
                "Margin": margin,
                "Trades": no_of_trades,
                "Profit": profit_percent
                }
            data.append(record)