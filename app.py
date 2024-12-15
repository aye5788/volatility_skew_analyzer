import streamlit as st
import pandas as pd
from src.fetch_data import fetch_options_data
from src.preprocess_data import preprocess_options_data
from src.interpret_skew import identify_calendar_opportunities, identify_butterfly_opportunities
from src.visualize import plot_skew_with_opportunities, plot_volatility_surface

st.title("Volatility Skew and Surface Analyzer")

# User Input
ticker = st.text_input("Enter Ticker Symbol:", value="AAPL")

if ticker:
    st.write(f"Fetching data for {ticker}...")
    
    # Fetch and preprocess options data
    calls_df, puts_df = fetch_options_data(ticker)
    calls_df = preprocess_options_data(calls_df)
    puts_df = preprocess_options_data(puts_df)

    # Debugging: Preview data
    st.write("Calls Data Preview")
    st.dataframe(calls_df.head())
    st.write("Puts Data Preview")
    st.dataframe(puts_df.head())

    # Allow user to select expiration date
    expirations = sorted(calls_df['expiration'].unique())
    selected_expiration = st.selectbox("Select Expiration Date:", expirations)

    # Filter data by selected expiration
    filtered_calls = calls_df[calls_df['expiration'] == selected_expiration]
    filtered_puts = puts_df[puts_df['expiration'] == selected_expiration]

    # Add a tab to switch between Volatility Skew and Volatility Surface
    tabs = st.tabs(["Volatility Skew", "Volatility Surface"])

    # Tab 1: Volatility Skew
    with tabs[0]:
        st.write("### Volatility Skew with Opportunities")
        calendar_opps = identify_calendar_opportunities(filtered_calls, filtered_puts)
        butterfly_opps = identify_butterfly_opportunities(filtered_calls)
        opportunities = calendar_opps + butterfly_opps

        # Plot skew
        plot_skew_with_opportunities(filtered_calls, filtered_puts, opportunities, st)

        # Display identified opportunities in a table
        if opportunities:
            st.write("### Identified Opportunities")
            opportunities_df = pd.DataFrame(opportunities)
            st.dataframe(opportunities_df)
        else:
            st.write("No opportunities found.")

    # Tab 2: Volatility Surface
    with tabs[1]:
        st.write("### Volatility Surface")
        plot_volatility_surface(calls_df, puts_df, st)
