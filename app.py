import streamlit as st
import pandas as pd
import re
from src.fetch_data import fetch_options_data
from src.preprocess_data import preprocess_options_data
from src.visualize import plot_skew_with_interpretation
from src.interpret_skew import identify_opportunities
st.set_page_config(layout="wide")

# Helper function to clean options data
def clean_options_data(df):
    df['expiry'] = df['contractSymbol'].apply(
        lambda x: re.search(r'(\d{6})', x).group(1) if re.search(r'(\d{6})', x) else None
    )
    df['expiry'] = pd.to_datetime(df['expiry'], format='%y%m%d', errors='coerce')
    df['ticker'] = df['contractSymbol'].apply(lambda x: re.split(r'(\d)', x, 1)[0])

    # Keep only relevant columns
    df = df[['ticker', 'expiry', 'strike', 'bid', 'ask', 'lastPrice', 'impliedVolatility']]
    df = df.rename(columns={'lastPrice': 'last_price'})
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

    # Allow user to select expiry date
    st.subheader("Select Expiry Date")
    unique_expiries = calls_data['expiry'].dropna().unique()
    selected_expiry = st.selectbox("Choose an expiry date:", unique_expiries)

    # Filter data based on selected expiry
    if selected_expiry:
        filtered_calls = calls_data[calls_data['expiry'] == selected_expiry]
        filtered_puts = puts_data[puts_data['expiry'] == selected_expiry]

        # Identify and display Butterfly Spread Opportunities
        st.subheader("Identified Butterfly Spread Opportunities")
        butterfly_opportunities = identify_opportunities(filtered_calls, filtered_puts)

        if butterfly_opportunities:
            opportunities_df = pd.DataFrame(butterfly_opportunities)
            st.dataframe(opportunities_df)
        else:
            st.write("No butterfly spread opportunities identified.")

        # Plot Volatility Skew
        st.subheader("Volatility Skew")
        plot_skew_with_interpretation(st, filtered_calls, filtered_puts)

        # Additional Interpretation
        st.subheader("Interpretation of the Skew")
        st.write("""
        The implied volatility skew highlights market sentiment:
        - **Higher IV for puts** indicates bearish sentiment, as traders are willing to pay more for downside protection.
        - **Higher IV for calls** may signal bullish sentiment or hedging activity.
        """)
