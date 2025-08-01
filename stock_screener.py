import requests
import time

# --- CONFIGURATION ---
# IMPORTANT: Replace 'YOUR_API_KEY' with your actual free API key from Alpha Vantage.
# Get your key here: https://www.alphavantage.co/support/#api-key
API_KEY = 'ULD2M2ARTXJFS70E'
SP500_SYMBOLS = [
    'A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'ATO', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXON', 'AXP', 'AZO', 'BA', 'BAC', 'BALL', 'BAX', 'BBWI', 'BBY', 'BDX', 'BEN', 'BF-B', 'BIIB', 'BIO', 'BK', 'BKNG', 'BKR', 'BLK', 'BLDR', 'BMY', 'BR', 'BRK-B', 'BRO', 'BSX', 'BWA', 'BX', 'BXP', 'C', 'CAG', 'CAH', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 'CDNS', 'CDW', 'CE', 'CEG', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 'COP', 'COST', 'CPB', 'CPRT', 'CPT', 'CRL', 'CRM', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTLT', 'CTRA', 'CTSH', 'CVS', 'CVX', 'CZR', 'D', 'DAL', 'DAY', 'DD', 'DE', 'DECK', 'DFRG', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'ELV', 'EMN', 'EMR', 'ENPH', 'EOG', 'EPAM', 'EQIX', 'EQR', 'EQT', 'ERIE', 'ES', 'ESS', 'ETN', 'ETR', 'ETSY', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FCX', 'FDS', 'FDX', 'FE', 'FFIV', 'FI', 'FICO', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRT', 'FSLR', 'FTNT', 'FTV', 'GD', 'GE', 'GEHC', 'GEN', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GRMN', 'GS', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUBB', 'HUM', 'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN', 'INCY', 'INTC', 'INTU', 'INVH', 'IP', 'IPG', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'J', 'JBL', 'JCI', 'JCP', 'JNJ', 'JNPR', 'JPM', 'K', 'KDP', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KVUE', 'L', 'LAD', 'LAMR', 'LDOS', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNT', 'LOW', 'LRCX', 'LULU', 'LUV', 'LVS', 'LW', 'LYB', 'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'META', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOH', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NI', 'NKE', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWS', 'NWSA', 'NXPI', 'O', 'ODFL', 'OKE', 'OMC', 'ON', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PANW', 'PARA', 'PAYC', 'PAYX', 'PCAR', 'PCG', 'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PODD', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX', 'RVTY', 'SBUX', 'SCHW', 'SEDG', 'SEE', 'SHW', 'SJM', 'SLB', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STLD', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TJX', 'TMO', 'TMUS', 'TPR', 'TRGP', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TXN', 'TXT', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VEEV', 'VFC', 'VICI', 'VLO', 'VMC', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ', 'WAB', 'WBD', 'WCN', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'WYNN', 'XEL', 'XOM', 'XRAY', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZTS'
]

def fetch_company_overview(symbol):
    """Fetches company overview data from Alpha Vantage."""
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching overview for {symbol}: {e}")
        return None

def fetch_time_series(symbol):
    """Fetches daily time series data from Alpha Vantage."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching time series for {symbol}: {e}")
        return None

def run_analysis_algorithm(overview_data, time_series_data):
    """
    Runs a crude algorithm to generate a score.
    Returns the score or None if analysis can't be run.
    """
    time_series = time_series_data.get('Time Series (Daily)')
    if not time_series:
        return None

    # Sort dates to ensure we have the latest data first
    dates = sorted(time_series.keys(), reverse=True)
    if len(dates) < 20:
        return None

    try:
        score = 0
        latest_close = float(time_series[dates[0]]['4. close'])
        five_days_ago_close = float(time_series[dates[4]]['4. close'])
        latest_volume = int(time_series[dates[0]]['5. volume'])

        recent_volumes = [int(time_series[date]['5. volume']) for date in dates[:20]]
        avg_volume = sum(recent_volumes) / len(recent_volumes)

        week_high_52 = float(overview_data.get('52WeekHigh', 0))
        week_low_52 = float(overview_data.get('52WeekLow', 0))
        pe_ratio_str = overview_data.get('PERatio', 'None')
        pe_ratio = float(pe_ratio_str) if pe_ratio_str != 'None' else 0

        # 1. Value based on 52-week range
        price_range = week_high_52 - week_low_52
        if price_range > 0 and ((latest_close - week_low_52) / price_range) < 0.25:
            score += 1

        # 2. Short-term momentum
        if latest_close > five_days_ago_close:
            score += 1

        # 3. P/E Ratio for value
        if 0 < pe_ratio < 20:
            score += 1

        # 4. Volume spike
        if latest_volume > avg_volume * 1.5:
            score += 1

        return score
    except (ValueError, TypeError, KeyError) as e:
        # Handle cases where data might be missing or in an unexpected format
        # print(f"Could not parse data for {overview_data.get('Symbol')}: {e}")
        return None


def main():
    """
    Main function to run the S&P 500 stock screener.
    """
    if API_KEY == 'YOUR_API_KEY':
        print("Error: Please replace 'YOUR_API_KEY' with your actual Alpha Vantage API key.")
        return

    print("--- Starting S&P 500 Stock Scan ---")
    print("WARNING: This scan will take a very long time (potentially over 1.5 hours) due to API rate limits.")

    all_scores = []
    total_symbols = len(SP500_SYMBOLS)

    for i, symbol in enumerate(SP500_SYMBOLS):
        print(f"Scanning {i + 1}/{total_symbols}: {symbol}...")

        overview_data = fetch_company_overview(symbol)
        time.sleep(1) # Small delay between the two calls for the same stock
        time_series_data = fetch_time_series(symbol)

        # Check for API rate limit message
        if (overview_data and ('Information' in overview_data or 'Note' in overview_data)) or \
           (time_series_data and ('Information' in time_series_data or 'Note' in time_series_data)):
            print("API rate limit likely reached. Pausing for 60 seconds...")
            time.sleep(60)
            # Retry the same symbol
            print(f"Retrying {symbol}...")
            overview_data = fetch_company_overview(symbol)
            time.sleep(1)
            time_series_data = fetch_time_series(symbol)

        if overview_data and time_series_data:
            score = run_analysis_algorithm(overview_data, time_series_data)
            if score is not None:
                all_scores.append({'symbol': symbol, 'score': score})
                print(f"  -> {symbol} scored: {score}")

        # IMPORTANT: Delay to respect API rate limits (e.g., 5 calls per minute)
        # 12 seconds between each symbol's analysis
        time.sleep(12)

    print("\n--- Scan Complete ---")

    # --- Display Results ---
    # Sort by score descending for buys
    all_scores.sort(key=lambda x: x['score'], reverse=True)
    print("\n--- Top 5 Potential Buys ---")
    for stock in all_scores[:5]:
        print(f"  {stock['symbol']}: Score {stock['score']}")

    # Sort by score ascending for sells/cautions
    all_scores.sort(key=lambda x: x['score'])
    print("\n--- Top 5 Stocks for Caution ---")
    for stock in all_scores[:5]:
        print(f"  {stock['symbol']}: Score {stock['score']}")

if __name__ == "__main__":
    main()
