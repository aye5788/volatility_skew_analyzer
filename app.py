import streamlit as st
import re
import pandas as pd
from src.fetch_data import fetch_options_data
from src.preprocess_data import preprocess_options_data
from src.visualize import plot_skew_with_opportunities
from src.interpret_skew import identify_opportunities

# Function to extract expiry dates from contractSymbol
def extract_expiry_from_symbol(df):
    df['expiry'] = df['contractSymbol'].apply(
        lambda x: re.search(r'(\d{6})', x).group(1) if re.search(r'(\d{6})', x) else None
    )
    df['expiry'] = pd.to_datetime(df['expiry'], format='%y%m%d', errors='coerce')
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

    # Extract expiry dates
    calls_data = extract_expiry_from_symbol(calls_data)
    puts_data = extract_expiry_from_symbol(puts_data)

    # Select Expiry Date
    unique_expiries = calls_data['expiry'].unique()
    st.subheader("Select Expiry Date")
    selected_expiry = st.selectbox("Choose Expiry Date:", options=unique_expiries)

    # Filter data based on the selected expiry date
    filtered_calls = calls_data[calls_data['expiry'] == selected_expiry]
    filtered_puts = puts_data[puts_data['expiry'] == selected_expiry]

    # Display filtered data
    st.write(f"### Calls Data for Expiry {selected_expiry}")
    st.dataframe(filtered_calls)

    st.write(f"### Puts Data for Expiry {selected_expiry}")
    st.dataframe(filtered_puts)

    # Identify Butterfly Spread Opportunities
    st.write("### Identified Butterfly Spread Opportunities")
    butterfly_opportunities = identify_opportunities(filtered_calls, filtered_puts)

    if butterfly_opportunities:
        st.dataframe(butterfly_opportunities)
    else:
        st.write("No butterfly spread opportunities identified.")

    # Plot Volatility Skew with Butterfly Opportunities
    st.subheader("Volatility Skew with Opportunities")
    plot_skew_with_opportunities(st, filtered_calls, filtered_puts, butterfly_opportunities)

