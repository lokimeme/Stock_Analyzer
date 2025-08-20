import yfinance as yf
import pandas as pd
from tqdm import tqdm

tickers_df = pd.read_csv("nasdaq.csv")
tickers = tickers_df["Ticker"].tolist()

removed = []
kept = []

for ticker in tqdm(tickers, desc="Checking tickers", unit="stock"):
    try:
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if data.empty:
            print(f"{ticker}: No data found, removing.")
            removed.append(ticker)
        else:
            kept.append(ticker)
    except Exception as e:
        if "No data found, symbol may be delisted" in str(e):
            print(f"{ticker}: Delisted, removing.")
            removed.append(ticker)
        else:
            print(f"{ticker}: Unexpected error ({e}), keeping for now.")
            kept.append(ticker)

new_df = tickers_df[tickers_df["Ticker"].isin(kept)]
new_df.to_csv("nasdaq.csv", index=False)

print(f"\nCleanup complete. {len(removed)} removed, {len(kept)} kept.")
if removed:
    print("Removed tickers:", removed)
