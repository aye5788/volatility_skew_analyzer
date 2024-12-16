def identify_opportunities(calls_df, puts_df, threshold=0.05):
    """
    Identifies butterfly spread opportunities based on implied volatility.
    """
    opportunities = []
    strikes = sorted(calls_df['strike'].unique())

    for i in range(1, len(strikes) - 1):
        lower_iv = calls_df[calls_df['strike'] == strikes[i - 1]]['impliedVolatility'].mean()
        middle_iv = calls_df[calls_df['strike'] == strikes[i]]['impliedVolatility'].mean()
        upper_iv = calls_df[calls_df['strike'] == strikes[i + 1]]['impliedVolatility'].mean()

        if middle_iv < lower_iv and middle_iv < upper_iv - threshold:
            opportunities.append({
                "body_strike": strikes[i],
                "wing_strikes": [strikes[i - 1], strikes[i + 1]],
                "opportunity_type": "Butterfly Spread",
                "lower_iv": round(lower_iv, 4),
                "middle_iv": round(middle_iv, 4),
                "upper_iv": round(upper_iv, 4),
            })

    return opportunities
