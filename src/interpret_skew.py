def identify_opportunities(calls_df, puts_df, threshold=0.05):
    """
    Identify opportunities for butterfly spreads with additional evaluation metrics.
    Includes calculations for net premium, max profit/loss, risk-reward, and collateral.
    Collateral reflects option contracts representing 100 shares.
    """
    opportunities = []
    strikes = sorted(calls_df['strike'].unique())

    for i in range(1, len(strikes) - 1):
        # Extract IVs for strikes
        lower_iv = calls_df[calls_df['strike'] == strikes[i - 1]]['impliedVolatility'].mean()
        middle_iv = calls_df[calls_df['strike'] == strikes[i]]['impliedVolatility'].mean()
        upper_iv = calls_df[calls_df['strike'] == strikes[i + 1]]['impliedVolatility'].mean()

        # Extract prices for strikes
        lower_bid = calls_df[calls_df['strike'] == strikes[i - 1]]['bid'].mean()
        middle_ask = calls_df[calls_df['strike'] == strikes[i]]['ask'].mean()
        upper_bid = calls_df[calls_df['strike'] == strikes[i + 1]]['bid'].mean()

        # Check for valid butterfly setup
        if lower_iv and middle_iv and upper_iv:
            if middle_iv < lower_iv and middle_iv < upper_iv - threshold:
                # Net premium (credit or debit)
                net_premium = lower_bid - 2 * middle_ask + upper_bid
                opportunity_type = "Credit" if net_premium > 0 else "Debit"

                # Collateral (strike price difference * 100 for 1 contract)
                collateral = (strikes[i + 1] - strikes[i - 1]) * 100

                # Max profit and loss
                max_profit = net_premium * 100 if net_premium > 0 else collateral + net_premium * 100
                max_loss = collateral - max_profit
                risk_reward = round(abs(max_profit / max_loss), 2) if max_loss != 0 else "N/A"

                # Append to opportunities
                opportunities.append({
                    "body_strike": strikes[i],
                    "wing_strikes": (strikes[i - 1], strikes[i + 1]),
                    "opportunity_type": f"Butterfly Spread ({opportunity_type})",
                    "net_premium": round(net_premium * 100, 2),
                    "max_profit": round(max_profit, 2),
                    "max_loss": round(max_loss, 2),
                    "risk_reward": risk_reward,
                    "collateral": round(collateral, 2),
                })

    return opportunities
