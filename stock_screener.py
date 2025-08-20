import os
import time
import math
import random
import pandas as pd
import numpy as np
import yfinance as yf
from tqdm import tqdm

TICKER_FILE = "russell1000_tickers.csv"
OUTPUT_FILE = "scan_results.csv"
FAILED_FILE = "failed_tickers.csv"

BATCH_SIZE = 10
BATCH_RETRIES = 6
SINGLE_RETRIES = 3
BASE_SLEEP = 5.0
JITTER = 2.0
SLEEP_BETWEEN_BATCHES = 0.5

def load_and_clean_tickers(path):
    df = pd.read_csv(path)
    symbols = (
        df["Ticker"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.replace("/", "-", regex=False)
        .str.replace(".", "-", regex=False)
        .str.replace(" ", "", regex=False)
    )
    symbols = [s for s in symbols if s and s != "NAN"]
    return sorted(set(symbols))

def calc_score(sym, df):
    if df is None or df.empty or len(df) < 21:
        return None
    d = df.copy()
    d["ma20"] = d["Close"].rolling(20).mean()
    score = 0
    if pd.notna(d["ma20"].iloc[-1]) and d["Close"].iloc[-1] < d["ma20"].iloc[-1]:
        dev = (d["ma20"].iloc[-1] - d["Close"].iloc[-1]) / d["ma20"].iloc[-1]
        if 0.02 < dev < 0.10:
            score += 3
    delta = d["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    if pd.notna(loss.iloc[-1]) and loss.iloc[-1] != 0:
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        if 30 < float(rsi.iloc[-1]) < 55:
            score += 3
    d["avg_volume_20"] = d["Volume"].rolling(20).mean()
    if pd.notna(d["avg_volume_20"].iloc[-1]) and pd.notna(d["Volume"].iloc[-1]):
        if d["Volume"].iloc[-1] > d["avg_volume_20"].iloc[-1] * 1.5:
            score += 2
    try:
        t, y = d.iloc[-1], d.iloc[-2]
        if (y["Close"] < y["Open"] and t["Close"] > t["Open"] and
            t["Close"] > y["Open"] and t["Open"] < y["Close"]):
            score += 2
    except Exception:
        pass
    return {"symbol": sym, "score": float(score)}

def has_data(df):
    if df is None or df.empty:
        return False
    needed = {"Open", "High", "Low", "Close", "Volume"}
    return isinstance(df.columns, pd.Index) and needed.issubset(df.columns)

def extract_frames(batch, data):
    out = {}
    if data is None or data.empty:
        for s in batch:
            out[s] = None
        return out
    if isinstance(data.columns, pd.MultiIndex):
        existing = set(data.columns.get_level_values(0))
        for s in batch:
            if s in existing:
                sub = data[s].dropna(how="all")
                out[s] = sub if has_data(sub) else None
            else:
                out[s] = None
    else:
        sub = data.dropna(how="all")
        for s in batch:
            out[s] = sub if has_data(sub) else None
    return out

def yf_download_batch(batch):
    return yf.download(
        tickers=batch,
        period="3mo",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        threads=False,
        progress=False,
        proxy=None,
        rounding=False,
    )

def download_with_backoff(batch, retries, base_sleep):
    wait = base_sleep
    for attempt in range(1, retries + 1):
        data = yf_download_batch(batch)
        frames = extract_frames(batch, data)
        ok = {s: df for s, df in frames.items() if df is not None and not df.empty}
        if len(ok) >= max(1, int(0.7 * len(batch))):
            return ok, [s for s in batch if s not in ok]
        if attempt < retries:
            time.sleep(wait + random.uniform(0, JITTER))
            wait *= 2
    return {s: df for s, df in frames.items() if df is not None and not df.empty}, [s for s, df in frames.items() if df is None or df.empty]

def download_single(sym):
    wait = BASE_SLEEP
    for attempt in range(1, SINGLE_RETRIES + 1):
        try:
            df = yf.download(
                tickers=sym,
                period="3mo",
                interval="1d",
                group_by="ticker",
                auto_adjust=True,
                threads=False,
                progress=False,
            )
            if has_data(df):
                return df
        except Exception:
            pass
        if attempt < SINGLE_RETRIES:
            time.sleep(wait + random.uniform(0, JITTER))
            wait *= 2
    return None

def main():
    symbols = load_and_clean_tickers(TICKER_FILE)
    if not symbols:
        print("No tickers.")
        return

    results = []
    failed = []
    total_batches = math.ceil(len(symbols) / BATCH_SIZE)

    pbar = tqdm(range(total_batches), desc="Batches", unit="batch")
    for i in pbar:
        batch = symbols[i * BATCH_SIZE : (i + 1) * BATCH_SIZE]
        ok_frames, to_fix = download_with_backoff(batch, BATCH_RETRIES, BASE_SLEEP)
        for s, df in ok_frames.items():
            res = calc_score(s, df)
            if res:
                results.append(res)
            else:
                to_fix.append(s)
        still_failed = []
        if to_fix:
            for s in to_fix:
                df = download_single(s)
                res = calc_score(s, df) if df is not None else None
                if res:
                    results.append(res)
                else:
                    still_failed.append(s)
                time.sleep(0.1)
        failed.extend(still_failed)

        if results:
            pd.DataFrame(results).sort_values("score", ascending=False).to_csv(OUTPUT_FILE, index=False)
        if failed:
            with open(FAILED_FILE, "w") as f:
                f.write("\n".join(failed))

        pbar.set_postfix(saved=len(results), failed=len(failed))
        time.sleep(SLEEP_BETWEEN_BATCHES)

    if results:
        ranked = pd.DataFrame(results).sort_values("score", ascending=False)
        ranked.to_csv(OUTPUT_FILE, index=False)
        print("\nTop 10:")
        print(ranked.head(10).to_string(index=False))
    else:
        print("No usable data. See failed tickers log.")

if __name__ == "__main__":
    main()

