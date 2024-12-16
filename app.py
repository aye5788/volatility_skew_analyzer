import streamlit as st
import pandas as pd
import re
from src.fetch_data import fetch_options_data
from src.preprocess_data import preprocess_options_data
from src.visualize import plot_skew_with_opportunities
from src.interpret_skew import identify_opportunities

# Helper function to clean options data
def clean_options_data(df):
    """
    Cleans options data by extracting ticker, expiry, and strike columns.
    Removes unnecessary columns for clarity.
    """
    # Extract expiry date from contractSymbol
    df['expiry'] = df['contractSymbol'].apply(
        lambda x: re.search(r'(\d{6})', x).group(1) if re.search(r'(\d{6})', x) else None
    )
    df['expiry'] = pd.to_datetime(df['expiry'], format='%y%m%d', errors='coerce')

    # Extract ticker (part before numeric in contractSymbol)
    df['ticker'] = df['contractSymbol'].apply(lambda x: re.split(r'(\d)', x, 1)[0])

    # Keep only relevant columns
    df = df[['ticker', 'expiry', 'strike', 'bid', 'ask', 'lastPrice', 'impliedVolatility']].copy()
    df = df.rename(columns={'lastPrice': 'last_price'})  # Rename for clarity
    
    return df

# Streamlit App Title
st.title("Volatility Skew and Surface Analyzer")

# User Input for Ticker Symbol
ticker = st.text_input("Enter Ticker Symbol:", value="AAPL")

if ticker:
    st.write(f"Fetching data for {ticker}...")

    # Fetch and preprocess options data
    options_data = fetch_options_data(ticker)
    if isinstance(options_data, tuple):
        calls_data, puts_data = options_data
    else:
        st.error("Error: `fetch_options_data` did not return expected tuple format.")
        st.stop()

    # Preprocess calls and puts data
    calls_data = preprocess_options_data(calls_data)
    puts_data = preprocess_options_data(puts_data)

    # Clean options data for better readability
    calls_data = clean_options_data(calls_data)
    puts_data = clean_options_data(puts_data)

    # Display cleaned Calls and Puts Data Preview
    st.subheader("Cleaned Calls Data Preview")
    st.dataframe(calls_data.head())

    st.subheader("Cleaned Puts Data Preview")
    st.dataframe(puts_data.head())

    # Allow user to select expiry date
    st.subheader("Select Expiry Date")
    unique_expiries = calls_data['expiry'].dropna().unique()
    selected_expiry = st.selectbox("Choose an expiry date:", unique_expiries)

    # Filter data based on selected expiry
    if selected_expiry:
        filtered_calls = calls_data[calls_data['expiry'] == selected_expiry]
        filtered_puts = puts_data[puts_data['expiry'] == selected_expiry]

        st.subheader(f"Filtered Calls Data for Expiry {selected_expiry}")
        st.dataframe(filtered_calls)

        st.subheader(f"Filtered Puts Data for Expiry {selected_expiry}")
        st.dataframe(filtered_puts)

        # Check for impliedVolatility column
        if 'impliedVolatility' not in filtered_calls.columns:
            st.warning("Missing 'impliedVolatility' column. Generating placeholder values.")
            filtered_calls['impliedVolatility'] = (filtered_calls['bid'] + filtered_calls['ask']) / 2
            filtered_puts['impliedVolatility'] = (filtered_puts['bid'] + filtered_puts['ask']) / 2

        # Identify Butterfly Spread Opportunities
        st.write("### Identified Butterfly Spread Opportunities")
        try:
            butterfly_opportunities = identify_opportunities(filtered_calls, filtered_puts)
            if butterfly_opportunities:
                st.dataframe(butterfly_opportunities)
            else:
                st.write("No butterfly spread opportunities identified.")
        except KeyError as e:
            st.error(f"Missing column error: {e}")

        # Plot Volatility Skew with Butterfly Opportunities
        st.subheader("Volatility Skew with Opportunities")
        plot_skew_with_opportunities(st, filtered_calls, filtered_puts, butterfly_opportunities)
