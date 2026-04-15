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
        "TotalPremium": ["count", "mean", "sum"],
        "Win": "mean",
        "T0APR": "mean",
        "TradeDurationDays": "mean"
    })

    result.columns = [
        "TradeCount",
        "AvgProfit",
        "TotalProfit",
        "WinRate",
        "AvgT0APR",
        "AvgDurationDays"
    ]

    result = result.reset_index()

    result["WinRate"] = result["WinRate"] * 100

    return result