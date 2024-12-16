import matplotlib.pyplot as plt
import seaborn as sns

def plot_skew_with_opportunities(st, filtered_calls, filtered_puts, opportunities):
    """
    Plots the implied volatility skew for calls and puts, highlighting butterfly spread opportunities.
    """
    # Check if DataFrames are empty
    if filtered_calls.empty or filtered_puts.empty:
        st.error("Error: One or both input DataFrames are empty.")
        return

    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot IV skew for calls and puts
    sns.lineplot(data=filtered_calls, x='strike', y='impliedVolatility', ax=ax, label="Calls IV", color="blue")
    sns.lineplot(data=filtered_puts, x='strike', y='impliedVolatility', ax=ax, label="Puts IV", color="red")

    # Highlight butterfly spread opportunities
    if opportunities:
        for opp in opportunities:
            ax.scatter(
                opp['body_strike'], 
                opp['middle_iv'], 
                color='purple', 
                s=50, 
                label="Butterfly Spread" if 'Butterfly Spread' in opp['opportunity_type'] else ""
            )

    # Add labels and legend
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Implied Volatility")
    ax.set_title("Volatility Skew with Opportunities")
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)
