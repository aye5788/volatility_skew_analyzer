import matplotlib.pyplot as plt

def plot_skew_with_interpretation(st, calls_df, puts_df):
    """
    Plot the implied volatility skew and provide interpretation for the skew.
    Adjust chart width dynamically without affecting other elements.
    """
    # Adjust chart width only (12 is the width, 6 is the height)
    fig, ax = plt.subplots(figsize=(12, 6))  

    # Plot Implied Volatility for Calls
    ax.plot(
        calls_df['strike'],
        calls_df['impliedVolatility'],
        marker='o',
        linestyle='-',
        label='Calls IV',
        color='tab:blue'
    )

    # Plot Implied Volatility for Puts
    ax.plot(
        puts_df['strike'],
        puts_df['impliedVolatility'],
        marker='o',
        linestyle='-',
        label='Puts IV',
        color='tab:orange'
    )

    # Titles and labels
    ax.set_title("Implied Volatility Skew")
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Implied Volatility")
    ax.legend()

    # Grid and layout adjustment
    ax.grid(True, linestyle='--', alpha=0.5)

    # Display the chart in Streamlit
    st.pyplot(fig)

    # Generate interpretation of the skew
    skew_interpretation = interpret_skew(calls_df, puts_df)
    st.subheader("Interpretation of the Skew")
    st.write(skew_interpretation)


def interpret_skew(calls_df, puts_df):
    """
    Generate a basic interpretation of the implied volatility skew.
    - Checks if puts IV > calls IV to infer bearish sentiment.
    """
    # Calculate the mean implied volatility for calls and puts
    avg_calls_iv = calls_df['impliedVolatility'].mean()
    avg_puts_iv = puts_df['impliedVolatility'].mean()

    # Compare average IVs to determine skew sentiment
    if avg_puts_iv > avg_calls_iv:
        return "The IV for puts is higher than calls. This may indicate a bearish sentiment."
    elif avg_calls_iv > avg_puts_iv:
        return "The IV for calls is higher than puts. This may indicate a bullish sentiment."
    else:
        return "The IV for calls and puts is roughly the same. Sentiment appears neutral."
