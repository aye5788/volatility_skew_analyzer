import matplotlib.pyplot as plt

def plot_skew_with_opportunities(calls_df, puts_df, opportunities):
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
