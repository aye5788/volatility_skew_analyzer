import matplotlib.pyplot as plt

def plot_skew_with_opportunities(st, filtered_calls, filtered_puts, opportunities):
    """
    Plots the implied volatility skew for calls and puts, highlighting opportunities.
    Cleaned-up version with better legend and clearer visualization.
    """
    # Check if DataFrames are empty
    if filtered_calls.empty or filtered_puts.empty:
        st.error("Error: One or both input DataFrames are empty.")
        return

    # Check if opportunities are empty
    if not opportunities:
        st.warning("No opportunities to display on the plot.")
        return
    
    try:
        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot IV skew for calls and puts
        ax.plot(
            filtered_calls['strike'], 
            filtered_calls['impliedVolatility'], 
            label="Calls IV", 
            color='blue',
            alpha=0.7
        )
        ax.plot(
            filtered_puts['strike'], 
            filtered_puts['impliedVolatility'], 
            label="Puts IV", 
            color='red',
            alpha=0.7
        )

        # Highlight butterfly spread opportunities
        body_strikes = []
        body_ivs = []

        for opp in opportunities:
            if 'body_strike' in opp and 'middle_iv' in opp:
                body_strikes.append(opp['body_strike'])
                body_ivs.append(opp['middle_iv'])

        # Plot butterfly opportunities as a single scatter plot
        if body_strikes and body_ivs:
            ax.scatter(
                body_strikes, 
                body_ivs, 
                color='purple', 
                s=50, 
                label="Butterfly Spread", 
                alpha=0.8
            )

        # Add labels and legend
        ax.set_xlabel("Strike Price")
        ax.set_ylabel("Implied Volatility")
        ax.set_title("Volatility Skew with Opportunities")
        ax.legend(loc="upper right")

        # Improve gridlines for better visibility
        ax.grid(True, linestyle="--", alpha=0.5)

        # Display the plot in Streamlit
        st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred while plotting: {e}")

