def identify_opportunities(calls_df, puts_df, threshold=0.05):
    """
    Identify opportunities for butterfly spreads.
    Adds a column specifying whether the opportunity is from Calls or Puts.
    """
    opportunities = []

    # Identify opportunities for Calls
    opportunities.extend(_find_butterfly_opportunities(calls_df, "Calls", threshold))

    # Identify opportunities for Puts
    opportunities.extend(_find_butterfly_opportunities(puts_df, "Puts", threshold))

    return opportunities


def _find_butterfly_opportunities(df, option_type, threshold):
    """
    Helper function to identify butterfly spreads for a given dataframe.
    """
    opportunities = []
    strikes = sorted(df['strike'].unique())

    # Loop through the strikes to identify butterfly spreads
    for i in range(1, len(strikes) - 1):
        lower_iv = df[df['strike'] == strikes[i - 1]]['impliedVolatility'].mean()
        middle_iv = df[df['strike'] == strikes[i]]['impliedVolatility'].mean()
        upper_iv = df[df['strike'] == strikes[i + 1]]['impliedVolatility'].mean()

        # Check for butterfly spread conditions
        if middle_iv < lower_iv and middle_iv < upper_iv - threshold:
            opportunities.append({
                "body_strike": strikes[i],
                "wing_strikes": [strikes[i - 1], strikes[i + 1]],
                "opportunity_type": f"Butterfly Spread ({option_type})",
                "lower_iv": round(lower_iv, 4),
                "middle_iv": round(middle_iv, 4),
                "upper_iv": round(upper_iv, 4),
            })

    return opportunities
