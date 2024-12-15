def identify_calendar_opportunities(calls_df, puts_df, iv_threshold=0.1):
    """
    Identify opportunities for calendar spreads.
    """
    opportunities = []
    for strike in sorted(calls_df['strike'].unique()):
        call_strikes = calls_df[calls_df['strike'] == strike]
        if len(call_strikes) > 1:
            short_iv = call_strikes['impliedVolatility'].iloc[0]
            long_iv = call_strikes['impliedVolatility'].iloc[-1]
            if short_iv > (long_iv + iv_threshold):
                opportunities.append({
                    "strike": strike,
                    "short_iv": short_iv,
                    "long_iv": long_iv,
                    "opportunity_type": "Calendar Spread"
                })
    return opportunities

def identify_butterfly_opportunities(calls_df, threshold=0.05):
    """
    Identify opportunities for butterfly spreads.
    """
    opportunities = []
    strikes = sorted(calls_df['strike'].unique())
    for i in range(1, len(strikes) - 1):
        lower_iv = calls_df[calls_df['strike'] == strikes[i - 1]]['impliedVolatility'].mean()
        middle_iv = calls_df[calls_df['strike'] == strikes[i]]['impliedVolatility'].mean()
        upper_iv = calls_df[calls_df['strike'] == strikes[i + 1]]['impliedVolatility'].mean()
        if middle_iv < lower_iv - threshold and middle_iv < upper_iv - threshold:
            opportunities.append({
                "body_strike": strikes[i],
                "wing_strikes": (strikes[i - 1], strikes[i + 1]),
                "opportunity_type": "Butterfly Spread",
                "lower_iv": lower_iv,
                "middle_iv": middle_iv,
                "upper_iv": upper_iv
            })
    return opportunities
