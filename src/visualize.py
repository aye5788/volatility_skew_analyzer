import matplotlib.pyplot as plt

def plot_skew_with_opportunities(st, filtered_calls, filtered_puts, opportunities):
    """
    Plots the implied volatility skew for calls and puts, highlighting opportunities.
    Includes debugging statements to verify data at each step.
    """
    # Debugging: Print the input DataFrames to check for issues
    st.write("### Debugging: Filtered Calls Data")
    st.dataframe(filtered_calls)
    st.write("### Debugging: Filtered Puts Data")
    st.dataframe(filtered_puts)
    st.write("### Debugging: Opportunities Data")
    st.json(opportunities)

    # Check if DataFrames are empty
    if filtered_calls.empty or filtered_puts.empty:
        st.error("Error: One or both input DataFrames are empty.")
        return

    # Check if opportunities are empty
    if not opportunities:
        st.warning("No opportunities to display on the plot.")
    
    # Create a figure
    try:
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot IV skew for calls and puts
        ax.plot(
            filtered_calls['strike'], 
            filtered_calls['impliedVolatility'], 
            label="Calls IV", 
            color='blue'
        )
        ax.plot(
            filtered_puts['strike'], 
            filtered_puts['impliedVolatility'], 
            label="Puts IV", 
            color='red'
        )

        # Highlight butterfly spread opportunities
        for opp in opportunities:
            if 'body_strike' in opp and 'middle_iv' in opp:
                ax.scatter(
                    opp['body_strike'], 
                    opp['middle_iv'], 
                    color='purple', 
                    s=50, 
                    label="Butterfly Spread" if 'Butterfly Spread' in opp['opportunity_type'] else ""
                )
            else:
                st.warning(f"Skipping opportunity with missing keys: {opp}")

        # Add labels and legend
        ax.set_xlabel("Strike Price")
        ax.set_ylabel("Implied Volatility")
        ax.set_title("Volatility Skew with Opportunities")
        ax.legend()

        # Display the plot in Streamlit
        st.pyplot(fig)
    except Exception as e:
        # Debugging: Print any exceptions
        st.error(f"An error occurred while plotting: {e}")
