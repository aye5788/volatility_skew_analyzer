import matplotlib.pyplot as plt
import pandas as pd

def plot_skew_with_interpretation(st, calls_df, puts_df):
    """
    Plots the implied volatility skew for calls and puts.
    Dynamically adjusts axis scaling and improves readability.

    Args:
        st: Streamlit object for display.
        calls_df (pd.DataFrame): DataFrame containing calls data.
        puts_df (pd.DataFrame): DataFrame containing puts data.
    """

    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot IV skew for calls and puts
    ax.plot(
        calls_df['strike'], 
        calls_df['impliedVolatility'], 
        label="Calls IV", 
        marker='o', 
        linestyle='-',
        color="tab:blue"
    )
    ax.plot(
        puts_df['strike'], 
        puts_df['impliedVolatility'], 
        label="Puts IV", 
        marker='o', 
        linestyle='-',
        color="tab:orange"
    )

    # Set dynamic x-axis scaling
    min_strike = min(calls_df['strike'].min(), puts_df['strike'].min())
    max_strike = max(calls_df['strike'].max(), puts_df['strike'].max())
    ax.set_xlim(min_strike - 5, max_strike + 5)  # Add a buffer around strikes

    # Improve readability
    ax.set_title("Implied Volatility Skew", fontsize=14)
    ax.set_xlabel("Strike Price", fontsize=12)
    ax.set_ylabel("Implied Volatility", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(fontsize=10)

    # Tighten layout
    plt.tight_layout()

    # Display plot
    st.pyplot(fig)

    # Interpretation of the skew
    st.subheader("Interpretation of the Skew")
    avg_call_iv = calls_df['impliedVolatility'].mean()
    avg_put_iv = puts_df['impliedVolatility'].mean()

    if avg_call_iv > avg_put_iv:
        st.write("The IV for calls is higher than puts. This may indicate a bullish sentiment.")
    elif avg_call_iv < avg_put_iv:
        st.write("The IV for puts is higher than calls. This may indicate a bearish sentiment.")
    else:
        st.write("The IV for calls and puts are similar. The market sentiment appears neutral.")
