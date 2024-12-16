import matplotlib.pyplot as plt
import pandas as pd

def plot_skew_with_interpretation(st, calls_df, puts_df):
    """
    Plots the implied volatility skew for calls and puts.
    Provides an interpretation based on the skew trend.

    Args:
        st: Streamlit object for display.
        calls_df (pd.DataFrame): DataFrame containing calls data.
        puts_df (pd.DataFrame): DataFrame containing puts data.
    """

    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot IV skew for calls and puts
    ax.plot(calls_df['strike'], calls_df['impliedVolatility'], label="Calls IV", marker='o')
    ax.plot(puts_df['strike'], puts_df['impliedVolatility'], label="Puts IV", marker='o')

    # Beautify chart
    ax.set_title("Implied Volatility Skew")
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Implied Volatility")
    ax.legend()
    ax.grid(True)

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

