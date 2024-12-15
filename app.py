import streamlit as st
import pandas as pd
from src.fetch_data import fetch_options_data
from src.preprocess_data import preprocess_options_data
from src.visualize import plot_skew_with_opportunities
from src.interpret_skew import identify_butterfly_opportunities

# Streamlit App
st.title("Volatility Skew and Surface Analyzer")

# Ticker input
ticker = st.text_input("Enter Ticker Symbol:", value="AAPL")
if ticker:
    st.write(f"Fetching data for {ticker}...")
    options_data = fetch_options_data(ticker)
    calls_data, puts_data = preprocess_options_data(options_data)
    
    # Show preview of the calls and puts data
    st.subheader("Calls Data Preview")
    st.dataframe(calls_data.head())
    
    st.subheader("Puts Data Preview")
    st.dataframe(puts_data.head())
    
    # Select expiration date
    expiration_dates = calls_data['expiration'].unique()
    selected_expiration = st.selectbox("Select Expiration Date:", expiration_dates)
    
    # Filter data for the selected expiration
    filtered_calls = calls_data[calls_data['expiration'] == selected_expiration]
    filtered_puts = puts_data[puts_data['expiration'] == selected_expiration]
    
    # Analyze butterfly opportunities
    stock_price = options_data['underlying_price'][0]
    stock_iv = options_data['impliedVolatility'][0] / 100  # Normalize to decimal
    opportunities = identify_butterfly_opportunities(filtered_calls, stock_price, stock_iv)
    
    # Plot volatility skew with opportunities
    st.subheader("Volatility Skew with Opportunities")
    plot_skew_with_opportunities(filtered_calls, filtered_puts, opportunities, st)
    
    # Display identified opportunities in a table
    if opportunities:
        st.write("### Identified Opportunities")
        opportunities_df = pd.DataFrame(opportunities)
        st.dataframe(opportunities_df)
    else:
        st.write("No opportunities found.")
