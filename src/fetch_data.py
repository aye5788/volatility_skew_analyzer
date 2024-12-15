import yfinance as yf
import pandas as pd

def fetch_options_data(ticker):
    """
    Fetch options data for a given ticker.
    Returns two DataFrames: calls and puts.
    """
    stock = yf.Ticker(ticker)
    expirations = stock.options
    calls_data, puts_data = [], []

    for exp in expirations:
        opt_chain = stock.option_chain(exp)
        calls = opt_chain.calls
        puts = opt_chain.puts
        calls['expiration'] = exp
        puts['expiration'] = exp
        calls_data.append(calls)
        puts_data.append(puts)

    calls_df = pd.concat(calls_data, ignore_index=True)
    puts_df = pd.concat(puts_data, ignore_index=True)
    return calls_df, puts_df
