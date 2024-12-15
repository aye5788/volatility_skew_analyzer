import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

def plot_skew_with_opportunities(calls_df, puts_df, opportunities, st):
    """
    Plots the volatility skew with strategy opportunities.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(calls_df['strike'], calls_df['impliedVolatility'], label="Calls", color="blue")
    plt.plot(puts_df['strike'], puts_df['impliedVolatility'], label="Puts", color="red")

    for opp in opportunities:
        if opp['opportunity_type'] == 'Calendar Spread':
            plt.scatter(opp['strike'], opp['short_iv'], color='green', label='Calendar Spread')
        elif opp['opportunity_type'] == 'Butterfly Spread':
            plt.scatter(opp['body_strike'], opp['middle_iv'], color='purple', label='Butterfly Spread')

    plt.title("Volatility Skew with Opportunities")
    plt.xlabel("Strike Price")
    plt.ylabel("Implied Volatility")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

def plot_volatility_surface(calls_df, puts_df, st):
    """
    Plots a 3D volatility surface for calls and puts combined.
    """
    combined = pd.concat([calls_df, puts_df])

    if combined.empty:
        st.write("No data available to plot the Volatility Surface.")
        return

    try:
        x = combined['strike']
        y = (combined['expiration'] - pd.Timestamp.now()).dt.days
        z = combined['impliedVolatility']

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(x, y, z, c=z, cmap="viridis", alpha=0.8)

        ax.set_title("Volatility Surface")
        ax.set_xlabel("Strike Price")
        ax.set_ylabel("Days to Expiration")
        ax.set_zlabel("Implied Volatility")
        fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
        st.pyplot(fig)
    except Exception as e:
        st.write("Error while plotting the Volatility Surface:", e)
