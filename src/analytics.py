import pandas as pd


def calculate_trade_summary(df):
    summaries = []

    for trade_id, group in df.groupby("TradeSequenceUUID"):
        group = group.sort_values("ExecutionDatetime").copy()

        entry_row = group.iloc[0]
        exit_row = group.iloc[-1]

        total_premium = group["Premium"].sum()
        trade_duration_days = (exit_row["ExecutionDatetime"] - entry_row["ExecutionDatetime"]).days

        days_to_exp = (entry_row["ExpirationDatetime"] - entry_row["ExecutionDatetime"]).days
        if days_to_exp <= 0:
            t0apr = 0
        else:
            t0apr = 100.0 * (entry_row["Price"] / entry_row["StrikePrice"]) * (365 / days_to_exp)

        if entry_row["Type"] == "Put":
            t0potm = 100.0 * (
                (entry_row["ExecutionQuote"] - entry_row["StrikePrice"])
                / entry_row["ExecutionQuote"]
            )
        else:
            t0potm = -100.0 * (
                (entry_row["ExecutionQuote"] - entry_row["StrikePrice"])
                / entry_row["ExecutionQuote"]
            )

        summaries.append({
            "TradeSequenceUUID": trade_id,
            "Stock": entry_row["Stock"],
            "Type": entry_row["Type"],
            "Positions": list(group["Position"]),
            "Quantity": entry_row["Quantity"],
            "StrikePrice": entry_row["StrikePrice"],
            "EntryPriceUnderlying": entry_row["ExecutionQuote"],
            "EntryOptionPrice": entry_row["Price"],
            "EntryDate": entry_row["ExecutionDatetime"],
            "ExitDate": exit_row["ExecutionDatetime"],
            "ExpirationDate": entry_row["ExpirationDatetime"],
            "TotalPremium": total_premium,
            "Win": total_premium > 0,
            "TradeDurationDays": trade_duration_days,
            "T0POTM": t0potm,
            "T0APR": t0apr,
        })

    summary = pd.DataFrame(summaries)
    return summary