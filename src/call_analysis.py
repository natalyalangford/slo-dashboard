import pandas as pd

def analyze_calls(summary_df, stocks=None):
    df = summary_df.copy()
    df = df[df["Type"] == "Call"].copy()

    if stocks is not None:
        df = df[df["Stock"].isin(stocks)].copy()

    if df.empty:
        return None

    results = {
        "total_trades": len(df),
        "called_away_rate": df["CalledAway"].mean() * 100,
        "avg_missed_upside": df["MissedUpside"].mean(),
        "median_missed_upside": df["MissedUpside"].median(),
        "avg_missed_upside_pct": df["MissedUpsidePct"].mean(),
        "median_missed_upside_pct": df["MissedUpsidePct"].median(),
        "avg_call_obligation": df["CallObligation"].mean(),
        "median_call_obligation": df["CallObligation"].median(),
        "avg_call_obligation_pct": df["CallObligationPct"].mean(),
        "median_call_obligation_pct": df["CallObligationPct"].median(),
        "avg_assignment_loss": df["AssignmentLoss"].mean(),
        "median_assignment_loss": df["AssignmentLoss"].median(),
        "max_assignment_loss": df["AssignmentLoss"].max(),
        "avg_total_loss": df["TotalLoss"].mean(),
        "median_total_loss": df["TotalLoss"].median(),
        "max_total_loss": df["TotalLoss"].max(),
        "avg_combined_loss": df["CombinedLoss"].mean(),
        "median_combined_loss": df["CombinedLoss"].median(),
        "max_combined_loss": df["CombinedLoss"].max(),
        "severe_event_rate": df["SevereEvent"].mean() * 100,
        "catastrophic_event_rate": df["CatastrophicEvent"].mean() * 100,
        "avg_close_apr": df["CloseAPR"].mean(),
        "median_close_apr": df["CloseAPR"].median(),
    }

    return results


def analyze_calls_by_potm(summary_df, stocks=None):
    df = summary_df.copy()
    df = df[df["Type"] == "Call"].copy()

    if stocks is not None:
        df = df[df["Stock"].isin(stocks)].copy()

    bins = [0, 5, 10, 15, 20, 30]
    labels = ["0-5%", "5-10%", "10-15%", "15-20%", "20-30%"]

    df["POTM_bucket"] = pd.cut(
        df["T0POTM"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    result = df.groupby("POTM_bucket", observed=False).agg({
        "TradeSequenceUUID": "count",
        "CalledAway": "mean",
        "MissedUpside": ["mean", "median", "max"],
        "MissedUpsidePct": ["mean", "median", "max"],
        "CallObligation": ["mean", "median", "max"],
        "CallObligationPct": ["mean", "median", "max"],
        "AssignmentLoss": ["mean", "median", "max"],
        "TotalLoss": ["mean", "median", "max"],
        "CombinedLoss": ["mean", "median", "max"],
        "SevereEvent": "mean",
        "CatastrophicEvent": "mean",
        "CloseAPR": ["mean", "median"],
    })

    result.columns = [
        "TradeCount",
        "CalledAwayRate",
        "AvgMissedUpside",
        "MedianMissedUpside",
        "MaxMissedUpside",
        "AvgMissedUpsidePct",
        "MedianMissedUpsidePct",
        "MaxMissedUpsidePct",
        "AvgCallObligation",
        "MedianCallObligation",
        "MaxCallObligation",
        "AvgCallObligationPct",
        "MedianCallObligationPct",
        "MaxCallObligationPct",
        "AvgAssignmentLoss",
        "MedianAssignmentLoss",
        "MaxAssignmentLoss",
        "AvgTotalLoss",
        "MedianTotalLoss",
        "MaxTotalLoss",
        "AvgCombinedLoss",
        "MedianCombinedLoss",
        "MaxCombinedLoss",
        "SevereEventRate",
        "CatastrophicEventRate",
        "AvgCloseAPR",
        "MedianCloseAPR",
    ]

    result["CalledAwayRate"] *= 100
    result["SevereEventRate"] *= 100
    result["CatastrophicEventRate"] *= 100

    return result.reset_index()


def find_best_call_zones(call_bucket_df, min_trades=5):
    df = call_bucket_df.copy()
    df = df[df["TradeCount"] >= min_trades].copy()

    if df.empty:
        return df

    df = df.sort_values(
        by=["AvgCombinedLoss", "CalledAwayRate", "MedianCloseAPR"],
        ascending=[True, True, False]
    )

    return df


def find_worst_call_zones(call_bucket_df, min_trades=5):
    df = call_bucket_df.copy()
    df = df[df["TradeCount"] >= min_trades].copy()

    if df.empty:
        return df

    df = df.sort_values(
        by=["MaxCombinedLoss", "AvgCombinedLoss", "CalledAwayRate"],
        ascending=[False, False, False]
    )

    return df

def get_potm_distribution(summary_df, stocks=None):
    df = summary_df.copy()
    df = df[df["Type"] == "Call"].copy()

    if stocks is not None:
        df = df[df["Stock"].isin(stocks)].copy()

    bins = [0, 5, 10, 15, 20, 30, 100]
    labels = ["0-5%", "5-10%", "10-15%", "15-20%", "20-30%", "30%+"]

    df["POTM_bucket"] = pd.cut(
        df["T0POTM"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    trade_counts = df["POTM_bucket"].value_counts().sort_index()
    percentages = df["POTM_bucket"].value_counts(normalize=True).sort_index() * 100

    result = pd.DataFrame({
        "TradeCount": trade_counts,
        "Percent": percentages
    })

    return result.reset_index()