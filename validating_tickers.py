import yfinance as yf
import pandas as pd

# Read the list of NSE tickers from a CSV file
tickers_df = pd.read_csv('EQUITY_L.csv')
tickers = tickers_df['SYMBOL'].tolist()

# Function to check if a ticker has data on Yahoo Finance
def verify_tickers(tickers):
    valid_tickers = []
    for ticker in tickers:
        yahoo_ticker = ticker + ".NS"  # Yahoo Finance uses '.NS' suffix for NSE stocks
        try:
            # Attempt to download data
            stock_data = yf.download(yahoo_ticker, period="1d")
            if not stock_data.empty:
                valid_tickers.append(ticker)
                print(f"Valid ticker: {ticker}")
            else:
                print(f"No data for ticker: {ticker}")
        except Exception as e:
            print(f"Error for ticker {ticker}: {e}")
    return valid_tickers

# Verify the tickers
valid_tickers = verify_tickers(tickers)

# Save the valid tickers to a CSV file
valid_tickers_df = pd.DataFrame(valid_tickers, columns=['Valid_Ticker'])
valid_tickers_df.to_csv('valid_nse_tickers.csv', index=False)

print("Verification complete. Valid tickers saved to 'valid_nse_tickers.csv'.")
