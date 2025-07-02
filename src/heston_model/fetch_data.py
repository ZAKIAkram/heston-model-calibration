import yfinance as yf
import datetime
import numpy as np
import pandas as pd
from pprint import pprint

import yfinance as yf
import pandas as pd
import numpy as np

def fetch_option_data(
    ticker: str,
    max_expirations: int = 5,
    strikes_per_exp: int = 7,
    strike_range: float = 0.25
) -> pd.DataFrame:
    """
    Fetch option data for a ticker, selecting a few expirations and strikes near ATM.

    Returns:
        pd.DataFrame with columns: strike, T (in years), impliedVolatility, option_type
    """
    yf_ticker = yf.Ticker(ticker)
    # spot_price = yf_ticker.history(period="1d")['Close'].iloc[-1]
    spot_price = yf_ticker.history(period="1d")['Close']
    if spot_price.empty:
        raise ValueError(f"No historical data available for {ticker}")
    spot_price = spot_price.iloc[-1]
    expirations = yf_ticker.options
    expirations_dt = pd.to_datetime(expirations)

    if len(expirations_dt) <= max_expirations:
        selected_expirations = expirations_dt
    else:
        idx = np.linspace(0, len(expirations_dt) - 1, max_expirations).astype(int)
        selected_expirations = expirations_dt[idx]

    all_options = []
    today = pd.Timestamp.today()

    for exp in selected_expirations:
        exp_str = exp.strftime('%Y-%m-%d')
        try:
            opt_chain = yf_ticker.option_chain(exp_str)
        except Exception:
            continue

        for option_type, option_df in [('call', opt_chain.calls), ('put', opt_chain.puts)]:
            df = option_df.copy()
            # df = df[(df['volume'] > 0) | (df['openInterest'] > 0)]
            df = df[df['openInterest'] > 0]
            df = df[df['impliedVolatility'].notna()]

            lower = spot_price * (1 - strike_range)
            upper = spot_price * (1 + strike_range)
            df = df[(df['strike'] >= lower) & (df['strike'] <= upper)]

            df = df.sort_values('strike')
            if len(df) > strikes_per_exp:
                idx = np.linspace(0, len(df) - 1, strikes_per_exp).astype(int)
                df = df.iloc[idx]

            if df.empty:
                continue

            df = df[['strike', 'impliedVolatility']].copy()
            df['expiration'] = exp
            df['T'] = (exp - today).days / 365.0
            df['option_type'] = option_type
            all_options.append(df)

    if not all_options:
        return pd.DataFrame(columns=['strike', 'T', 'impliedVolatility', 'option_type'])
    result = pd.concat(all_options, ignore_index=True)
    result = result[result['T'] > 1e-4]  
    result = result.dropna()
    return result[['strike', 'T', 'impliedVolatility', 'option_type']]




def main():
    ticker = "AAPL"
    print(f"Fetching option data for {ticker}...")

    try:
        df = fetch_option_data(ticker)

        if df.empty:
            print("No valid option data was found.")
        else:
            print(f"\nFetched {len(df)} options:")
            print(df.head(10))  # Show first 10 rows
    except Exception as e:
        print("Error fetching options:", str(e))

if __name__ == "__main__":
    main()