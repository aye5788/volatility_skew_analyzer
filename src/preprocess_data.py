import pandas as pd

def preprocess_options_data(options_df):
    """
    Preprocesses the options DataFrame:
    - Converts expiration to datetime format
    - Filters rows with invalid or non-positive implied volatility
    """
    if not isinstance(options_df, pd.DataFrame):
        raise ValueError("Input to `preprocess_options_data` must be a DataFrame.")
    
    options_df['expiration'] = pd.to_datetime(options_df['expiration'])
    options_df['impliedVolatility'] = options_df['impliedVolatility'].astype(float)
    options_df = options_df[options_df['impliedVolatility'] > 0]  # Keep only positive IV
    options_df['strike'] = options_df['strike'].astype(float)
    return options_df
