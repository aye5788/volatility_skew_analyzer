import streamlit as st
from src.fetch_data import fetch_options_data
from src.preprocess_data import preprocess_options_data
from src.interpret_skew import identify_opportunities
from src.visualize import plot_skew_with_opportunities

# Streamlit app title
st.title("Volatility Skew and Surface Analyzer")

# User input for ticker symbol
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

    # Preprocess the data
    calls_data = preprocess_options_data(calls_data)
    puts_data = preprocess_options_data(puts_data)

    # Display Calls and Puts Data Preview
    st.subheader("Calls Data Preview")
    st.dataframe(calls_data.head())

    st.subheader("Puts Data Preview")
    st.dataframe(puts_data.head())

    # Identify Butterfly Opportunities
    st.write("### Analyzing for Butterfly Spread Opportunities...")
    opportunities = identify_opportunities(calls_data, puts_data)

    # Display and visualize opportunities
    if opportunities:
        st.write("### Identified Butterfly Spread Opportunities")
        st.dataframe(opportunities)

        st.write("### Volatility Skew with Opportunities")
        plot_skew_with_opportunities(st, calls_data, puts_data, opportunities)
    else:
        st.write("No butterfly spread opportunities identified.")
