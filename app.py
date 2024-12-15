import pandas as pd
import streamlit as st
from src.preprocess_data import preprocess_options_data
from src.visualize import plot_skew_with_opportunities
from src.calculate_metrics import calculate_opportunity_metrics

st.title("Volatility Skew and Surface Analyzer")

ticker = st.text_input("Enter Ticker Symbol:", value="AAPL")

if ticker:
    st.write(f"Fetching data for {ticker}...")
    
    # Fetch and preprocess options data
    options_data = fetch_options_data(ticker)  # Ensure this function returns correctly structured data
    if isinstance(options_data, tuple):
        calls_data, puts_data = options_data  # Unpack tuple
    else:
        st.error("Error: `fetch_options_data` did not return expected tuple format.")
        st.stop()

    calls_data = preprocess_options_data(calls_data)
    puts_data = preprocess_options_data(puts_data)

    # Display preview of the calls and puts data
    st.subheader("Calls Data Preview")
    st.dataframe(calls_data.head())
    st.subheader("Puts Data Preview")
    st.dataframe(puts_data.head())

    # Calculate and display opportunities
    opportunities = calculate_opportunity_metrics(calls_data, puts_data)
    if opportunities:
        st.write("### Identified Opportunities")
        st.dataframe(opportunities)
    else:
        st.write("No opportunities identified.")

