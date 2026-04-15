def calculate_metrics(summary_df):
    total_trades = len(summary_df)
    total_profit = summary_df["TotalPremium"].sum()
    win_rate = summary_df["Win"].mean()

    avg_profit = summary_df["TotalPremium"].mean()
    avg_duration = summary_df["TradeDurationDays"].mean()

    best_trade = summary_df["TotalPremium"].max()
    worst_trade = summary_df["TotalPremium"].min()

    return {
        "total_trades": total_trades,
        "total_profit": total_profit,
        "win_rate": win_rate,
        "avg_profit": avg_profit,
        "avg_duration": avg_duration,
        "best_trade": best_trade,
        "worst_trade": worst_trade
    }