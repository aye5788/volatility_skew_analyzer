import pandas as pd

def preprocess_options_data(options_df):
    """
    Preprocess the options data:
    - Converts expiration to datetime format
    - Ensures impliedVolatility values are valid (filters out non-positive IVs)
    - Returns cleaned DataFrame
    """
    # Convert expiration column to datetime
    options_df['expiration'] = pd.to_datetime(options_df['expiration'])

    # Ensure impliedVolatility is a float and filter out invalid rows
    options_df['impliedVolatility'] = options_df['impliedVolatility'].astype(float)
    options_df = options_df[options_df['impliedVolatility'] > 0]  # Keep only valid IVs

    # Ensure that strike prices are numeric
    options_df['strike'] = options_df['strike'].astype(float)

    return options_df
    
