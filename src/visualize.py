import matplotlib.pyplot as plt

def plot_skew_with_opportunities(filtered_calls, filtered_puts, opportunities, st):
    fig, ax = plt.subplots(figsize=(10, 6))
print("Type of filtered_calls:", type(filtered_calls))
print("filtered_calls content:", filtered_calls)
print("Type of filtered_puts:", type(filtered_puts))
print("filtered_puts content:", filtered_puts)
    
    # Plot IV skew
        ax.plot(filtered_calls['strike'], filtered_calls['impliedVolatility'], label="Calls", color="blue")
        ax.plot(filtered_puts['strike'], filtered_puts['impliedVolatility'], label="Puts", color="red")
    
    # Highlight butterfly spread opportunities
    for opp in opportunities:
        ax.scatter(
            opp['body_strike'], 
            opp['middle_iv'], 
            label=f"Butterfly Spread", 
            color="purple", 
            s=50
        )
    
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Implied Volatility")
    ax.set_title("Volatility Skew with Opportunities")
    ax.legend()
    st.pyplot(fig)

