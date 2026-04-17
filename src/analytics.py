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

        # Entry metrics
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

        capital = entry_row["StrikePrice"] * 100 * entry_row["Quantity"]

        if capital == 0:
            realized_return_pct = 0
        else:
            realized_return_pct = 100.0 * (total_premium / capital)

        if trade_duration_days <= 0:
            close_apr = 0
        else:
            close_apr = realized_return_pct * (365 / trade_duration_days)

        # Exit underlying price
        exit_price_underlying = exit_row["ExecutionQuote"]

        # Call-analysis fields
        called_away = exit_price_underlying > entry_row["StrikePrice"]

        missed_upside = max(
            0,
            exit_price_underlying - entry_row["StrikePrice"]
        ) * 100 * entry_row["Quantity"]

        missed_upside_pct = max(
            0,
            (exit_price_underlying - entry_row["StrikePrice"]) / entry_row["StrikePrice"]
        ) * 100

        call_obligation = missed_upside
        call_obligation_pct = missed_upside_pct

        # Assignment loss
        # Only applies to call trades that were assigned
        if entry_row["Type"] == "Call" and "Assign" in group["Position"].values:
            intrinsic_value = max(
                0,
                exit_price_underlying - entry_row["StrikePrice"]
            ) * 100 * entry_row["Quantity"]

            assignment_loss = intrinsic_value - total_premium
        else:
            assignment_loss = 0

        # Unified loss metric (captures ALL downside)
        if total_premium < 0:
            total_loss = abs(total_premium)
        else:
            total_loss = 0

        # Combine assignment + buy-to-close risk
        combined_loss = max(assignment_loss, total_loss)

        # Tail-risk flags
        severe_event = missed_upside_pct >= 20
        catastrophic_event = missed_upside_pct >= 50

        summaries.append({
            "TradeSequenceUUID": trade_id,
            "Stock": entry_row["Stock"],
            "Type": entry_row["Type"],
            "Positions": list(group["Position"]),
            "Quantity": entry_row["Quantity"],
            "StrikePrice": entry_row["StrikePrice"],
            "EntryPriceUnderlying": entry_row["ExecutionQuote"],
            "ExitPriceUnderlying": exit_price_underlying,
            "EntryOptionPrice": entry_row["Price"],
            "EntryDate": entry_row["ExecutionDatetime"],
            "ExitDate": exit_row["ExecutionDatetime"],
            "ExpirationDate": entry_row["ExpirationDatetime"],
            "TotalPremium": total_premium,
            "Win": total_premium > 0,
            "TradeDurationDays": trade_duration_days,
            "Capital": capital,
            "T0POTM": t0potm,
            "T0APR": t0apr,
            "RealizedReturnPct": realized_return_pct,
            "CloseAPR": close_apr,
            "CalledAway": called_away,
            "MissedUpside": missed_upside,
            "MissedUpsidePct": missed_upside_pct,
            "CallObligation": call_obligation,
            "CallObligationPct": call_obligation_pct,
            "AssignmentLoss": assignment_loss,
            "SevereEvent": severe_event,
            "CatastrophicEvent": catastrophic_event,
            "TotalLoss": total_loss,
            "CombinedLoss": combined_loss,
        })

    summary = pd.DataFrame(summaries)
    return summary