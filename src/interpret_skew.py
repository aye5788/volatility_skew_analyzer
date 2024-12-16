def identify_opportunities(calls_df, puts_df, threshold=0.05):
    """
    Identify opportunities for butterfly spreads with metrics and option type.
    """
    opportunities = []

    # Identify opportunities for Calls
    opportunities.extend(_find_butterfly_opportunities(calls_df, "Calls", threshold))

    # Identify opportunities for Puts
    opportunities.extend(_find_butterfly_opportunities(puts_df, "Puts", threshold))

    return pd.DataFrame(opportunities)


def _find_butterfly_opportunities(df, option_type, threshold):
    """
    Helper function to identify butterfly spreads for a given dataframe.
    """
    opportunities = []
    strikes = sorted(df['strike'].unique())

    for i in range(1, len(strikes) - 1):
        # Calculate IV for wing and body strikes
        lower_iv = df[df['strike'] == strikes[i - 1]]['impliedVolatility'].mean()
        middle_iv = df[df['strike'] == strikes[i]]['impliedVolatility'].mean()
        upper_iv = df[df['strike'] == strikes[i + 1]]['impliedVolatility'].mean()

        # Ensure it meets butterfly spread conditions
        if middle_iv < lower_iv and middle_iv < upper_iv - threshold:
            # Example premium values for simplicity
            net_premium = round((lower_iv + upper_iv - 2 * middle_iv) * 100, 2)  # Mock premium calc
            max_profit = abs(net_premium)  # Max profit = premium for debit or credit
            max_loss = abs(100 - net_premium)  # Mock loss calc
            risk_reward = round(max_profit / max_loss, 2) if max_loss != 0 else float('inf')
            collateral = 100 * 2  # Assuming 2x spread width in dollars (RH logic)

            opportunities.append({
                "body_strike": strikes[i],
                "wing_strikes": [strikes[i - 1], strikes[i + 1]],
                "opportunity_type": f"Butterfly Spread ({option_type})",
                "lower_iv": round(lower_iv, 4),
                "middle_iv": round(middle_iv, 4),
                "upper_iv": round(upper_iv, 4),
                "net_premium": net_premium,
                "max_profit": max_profit,
                "max_loss": -max_loss,
                "risk_reward": risk_reward,
                "collateral": collateral
            })

    return opportunities
