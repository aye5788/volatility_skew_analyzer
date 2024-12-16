def identify_opportunities(calls_df, puts_df, threshold=0.05):
    """
    Identify butterfly spread opportunities with metrics:
    - Net Premium (Credit/Debit)
    - Max Profit
    - Max Loss
    - Risk-to-Reward Ratio
    - Expected Collateral
    - Breakevens
    """
    opportunities = []
    strikes = sorted(calls_df['strike'].unique())

    # Loop through strikes to find butterfly spreads
    for i in range(1, len(strikes) - 1):
        lower_strike = strikes[i - 1]
        body_strike = strikes[i]
        upper_strike = strikes[i + 1]

        # Calculate IVs and prices (use midpoint between bid/ask as price)
        lower_iv = calls_df[calls_df['strike'] == lower_strike]['impliedVolatility'].mean()
        middle_iv = calls_df[calls_df['strike'] == body_strike]['impliedVolatility'].mean()
        upper_iv = calls_df[calls_df['strike'] == upper_strike]['impliedVolatility'].mean()
        
        lower_price = calls_df[calls_df['strike'] == lower_strike][['bid', 'ask']].mean(axis=1).mean()
        body_price = calls_df[calls_df['strike'] == body_strike][['bid', 'ask']].mean(axis=1).mean()
        upper_price = calls_df[calls_df['strike'] == upper_strike][['bid', 'ask']].mean(axis=1).mean()

        # Calculate Net Premium
        net_premium = round(lower_price + upper_price - 2 * body_price, 2)

        # Determine Strike Width
        strike_width = round(upper_strike - body_strike, 2)

        # Max Profit, Max Loss, and Collateral
        if net_premium > 0:  # Credit Butterfly
            max_profit = net_premium
            max_loss = strike_width - net_premium
        else:  # Debit Butterfly
            max_profit = strike_width + net_premium  # net_premium is negative here
            max_loss = -net_premium

        risk_to_reward = round(max_loss / max_profit, 2) if max_profit != 0 else None
        collateral = strike_width  # Robinhood requirement for credit spreads

        # Append opportunity if valid
        if middle_iv < lower_iv and middle_iv < upper_iv - threshold:
            opportunities.append({
                "body_strike": body_strike,
                "wing_strikes": (lower_strike, upper_strike),
                "opportunity_type": "Butterfly Spread",
                "net_premium": net_premium,
                "max_profit": round(max_profit, 2),
                "max_loss": round(max_loss, 2),
                "risk_to_reward": risk_to_reward,
                "collateral": collateral,
                "breakevens": (
                    round(lower_strike + abs(net_premium), 2),
                    round(upper_strike - abs(net_premium), 2)
                )
            })

    return opportunities
