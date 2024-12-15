import streamlit as st
from src.fetch_data import fetch_options_data
from src.preprocess_data import preprocess_options_data
from src.visualize import plot_skew_with_opportunities
from src.interpret_skew import identify_calendar_opportunities, identify_butterfly_opportunities

st.title("Volatility Skew and Surface Analyzer")

# Input Ticker
ticker = st.text_input("Enter Ticker Symbol:", value="AAPL")

if ticker:
    st.write(f"Fetching data for {ticker}...")
    
    # Fetch and preprocess data
    options_data = fetch_options_data(ticker)
    if isinstance(options_data, tuple):
        calls_data, puts_data = options_data
    else:
        st.error("Error: `fetch_options_data` did not return expected tuple format.")
        st.stop()

    calls_data = preprocess_options_data(calls_data)
    puts_data = preprocess_options_data(puts_data)

    # Display Preview
    st.subheader("Calls Data Preview")
    st.dataframe(calls_data.head())

    st.subheader("Puts Data Preview")
    st.dataframe(puts_data.head())

    # Calculate opportunities
    calendar_opps = identify_calendar_opportunities(calls_data, puts_data)
    butterfly_opps = identify_butterfly_opportunities(calls_data)

    opportunities = calendar_opps + butterfly_opps

    # Visualize and Display
    st.subheader("Volatility Skew with Opportunities")
    plot_skew_with_opportunities(st, calls_data, puts_data, opportunities)

    # Display identified opportunities
    if opportunities:
        st.write("### Identified Opportunities")
        st.dataframe(opportunities)
    else:
        st.write("No opportunities identified.")
