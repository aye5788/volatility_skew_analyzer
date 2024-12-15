import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

def plot_skew_with_opportunities(calls_df, puts_df, opportunities):
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
    plt.show()

def plot_volatility_surface(calls_df, puts_df):
    """
    Plots a 3D volatility surface for calls and puts combined.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    combined = pd.concat([calls_df, puts_df])
    x = combined['strike']
    y = (combined['expiration'] - pd.Timestamp.now()).dt.days
    z = combined['impliedVolatility']

    ax.scatter(x, y, z, c=z, cmap="viridis", alpha=0.8)
    ax.set_title("Volatility Surface")
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Days to Expiration")
    ax.set_zlabel("Implied Volatility")
    plt.colorbar(ax.scatter(x, y, z, c=z, cmap="viridis"))
    plt.show()
