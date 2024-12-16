import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_skew_with_interpretation(st, calls_data, puts_data):
    """
    Plots the implied volatility skew for calls and puts and outputs an interpretation.
    """

    # Check if data exists
    if calls_data.empty or puts_data.empty:
        st.error("No data available to plot.")
        return

    # Initialize the figure
    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")

    # Sort data by strike price for better readability
    calls_data = calls_data.sort_values(by="strike")
    puts_data = puts_data.sort_values(by="strike")

    # Plot calls and puts IV skew
    plt.plot(
        calls_data['strike'], calls_data['impliedVolatility'], 
        label='Calls IV', color='blue', linewidth=1.5
    )
    plt.plot(
        puts_data['strike'], puts_data['impliedVolatility'], 
        label='Puts IV', color='red', linewidth=1.5
    )

    # Add chart details
    plt.title("Implied Volatility Skew")
    plt.xlabel("Strike Price")
    plt.ylabel("Implied Volatility")
    plt.legend()
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Interpretation logic
    interpret_skew(st, calls_data, puts_data)


def interpret_skew(st, calls_data, puts_data):
    """
    Outputs an interpretation of the volatility skew.
    """

    call_skew = np.polyfit(calls_data['strike'], calls_data['impliedVolatility'], 1)[0]
    put_skew = np.polyfit(puts_data['strike'], puts_data['impliedVolatility'], 1)[0]

    st.subheader("Volatility Skew Interpretation")

    def get_interpretation(skew, option_type):
        if skew > 0:
            return f"The {option_type} skew is upward sloping, indicating higher IV for OTM options. This suggests hedging demand or market fear."
        elif skew < 0:
            return f"The {option_type} skew is downward sloping, indicating higher IV for ITM options. This suggests supply or market complacency."
        else:
            return f"The {option_type} skew is flat, indicating balanced demand across strikes."

    # Display interpretation
    st.write(get_interpretation(call_skew, "calls"))
    st.write(get_interpretation(put_skew, "puts"))

