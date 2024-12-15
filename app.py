import streamlit as st
from src.fetch_data import fetch_options_data
from src.preprocess_data import preprocess_options_data
from src.interpret_skew import identify_calendar_opportunities, identify_butterfly_opportunities
from src.visualize import plot_skew_with_opportunities

st.title("Volatility Skew Analyzer")

ticker = st.text_input("Enter Ticker Symbol:", value="AAPL")

if ticker:
    # Fetch options data
    calls_df, puts_df = fetch_options_data(ticker)
    calls_df = preprocess_options_data(calls_df)
    puts_df = preprocess_options_data(puts_df)

    # Select expiration
    expirations = sorted(calls_df['expiration'].unique())
    selected_expiration = st.selectbox("Select Expiration Date:", expirations)

    # Filter data by expiration
    calls_df = calls_df[calls_df['expiration'] == selected_expiration]
    puts_df = puts_df[puts_df['expiration'] == selected_expiration]

    # Identify opportunities
    calendar_opps = identify_calendar_opportunities(calls_df, puts_df)
    butterfly_opps = identify_butterfly_opportunities(calls_df)
    opportunities = calendar_opps + butterfly_opps

    # Plot skew with opportunities
    st.write("### Volatility Skew with Opportunities")
    plot_skew_with_opportunities(calls_df, puts_df, opportunities)

    # Display opportunities in a table
    st.write("### Identified Opportunities")
    st.write(opportunities)
