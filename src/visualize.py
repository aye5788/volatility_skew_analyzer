import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.ndimage import uniform_filter1d

def plot_skew_with_opportunities(st, filtered_calls, filtered_puts, opportunities):
    """
    Plots the implied volatility skew for calls and puts, highlighting butterfly opportunities.
    Includes smoothing and filtering for a clean, professional look.
    """
    # Ensure the seaborn style is used for aesthetics
    sns.set_theme(style="whitegrid")

    # Check if DataFrames are empty
    if filtered_calls.empty or filtered_puts.empty:
        st.error("Error: One or both input DataFrames are empty.")
        return

    # Filter out IV values that are unrealistic (e.g., negative or too high)
    filtered_calls = filtered_calls[(filtered_calls['impliedVolatility'] > 0) & 
                                    (filtered_calls['impliedVolatility'] < 5)]
    filtered_puts = filtered_puts[(filtered_puts['impliedVolatility'] > 0) & 
                                  (filtered_puts['impliedVolatility'] < 5)]

    # Smooth the IV curves using a rolling average
    def smooth_iv(data):
        return uniform_filter1d(data, size=5)  # 5-point moving average

    try:
        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 6))

        # Smooth and plot calls IV
        calls_strikes = filtered_calls['strike']
        calls_iv = smooth_iv(filtered_calls['impliedVolatility'])
        ax.plot(
            calls_strikes, calls_iv, 
            label="Calls IV", 
            color='blue', linewidth=2, alpha=0.8
        )

        # Smooth and plot puts IV
        puts_strikes = filtered_puts['strike']
        puts_iv = smooth_iv(filtered_puts['impliedVolatility'])
        ax.plot(
            puts_strikes, puts_iv, 
            label="Puts IV", 
            color='red', linewidth=2, alpha=0.8
        )

        # Plot butterfly spread opportunities
        if opportunities:
            body_strikes = [opp['body_strike'] for opp in opportunities if 'body_strike' in opp]
            body_ivs = [opp['middle_iv'] for opp in opportunities if 'middle_iv' in opp]
            ax.scatter(
                body_strikes, body_ivs, 
                color='purple', 
                s=60, 
                label="Butterfly Spread", 
                edgecolor='white', alpha=0.9
            )

        # Set axis labels, title, and grid
        ax.set_xlabel("Strike Price")
        ax.set_ylabel("Implied Volatility")
        ax.set_title("Volatility Skew with Opportunities")
        ax.legend(loc="upper right")
        ax.grid(visible=True, linestyle="--", alpha=0.5)

        # Limit X and Y axes for better focus
        ax.set_xlim(calls_strikes.min(), calls_strikes.max())
        ax.set_ylim(0, 5)  # Limiting IV to a cleaner range

        # Display the plot in Streamlit
        st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred while plotting: {e}")
