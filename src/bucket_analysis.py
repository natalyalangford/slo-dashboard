import pandas as pd


def analyze_potm_buckets(summary_df):
    df = summary_df.copy()

    bins = [0, 2, 5, 10, 15, 20, 100]
    labels = ["0-2%", "2-5%", "5-10%", "10-15%", "15-20%", "20%+"]

    df["POTM_bucket"] = pd.cut(
        df["T0POTM"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    result = df.groupby("POTM_bucket", observed=False).agg({
        "TotalPremium": ["count", "mean", "median", "sum", "min", "max"],
        "Win": "mean",
        "T0APR": ["mean", "median"],
        "CloseAPR": ["mean", "median"],
        "RealizedReturnPct": ["mean", "median"],
        "TradeDurationDays": "mean"
    })

    result.columns = [
        "TradeCount",
        "AvgProfit",
        "MedianProfit",
        "TotalProfit",
        "WorstTrade",
        "BestTrade",
        "WinRate",
        "AvgT0APR",
        "MedianT0APR",
        "AvgCloseAPR",
        "MedianCloseAPR",
        "AvgRealizedReturnPct",
        "MedianRealizedReturnPct",
        "AvgDurationDays"
    ]

    result = result.reset_index()
    result["WinRate"] = result["WinRate"] * 100

    return result