import pandas as pd

def preprocess_options_data(df):
    """
    Preprocess options data to retain relevant columns and drop missing values.
    """
    # Retain necessary columns
    necessary_columns = ['contractSymbol', 'strike', 'bid', 'ask', 'lastPrice', 'impliedVolatility']
    df = df[necessary_columns].copy()

    # Drop rows with missing strike or impliedVolatility
    df.dropna(subset=['strike', 'impliedVolatility'], inplace=True)
    
    return df
