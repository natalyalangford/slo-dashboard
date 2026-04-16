import pandas as pd

def add_analysis_buckets(summary_df):
    df = summary_df.copy()

    df = df[df["Stock"].isin(["SOXL", "TQQQ"])].copy()

    # 🔹 POTM (4 bins)
    potm_bins = [0, 5, 10, 15, 100]
    potm_labels = ["0-5%", "5-10%", "10-15%", "15%+"]

    df["T0POTM_bucket"] = pd.cut(
        df["T0POTM"],
        bins=potm_bins,
        labels=potm_labels,
        include_lowest=True
    )

    # 🔹 APR (3 bins)  ← NEW
    apr_bins = [0, 40, 80, 1000]
    apr_labels = ["0-40", "40-80", "80+"]

    df["T0APR_bucket"] = pd.cut(
        df["T0APR"],
        bins=apr_bins,
        labels=apr_labels,
        include_lowest=True
    )

    return df


def build_heatmap_tables(df, stock, option_type):
    subset = df[(df["Stock"] == stock) & (df["Type"] == option_type)].copy()

    avg_close_apr = pd.pivot_table(
        subset,
        index="T0POTM_bucket",
        columns="T0APR_bucket",
        values="CloseAPR",
        aggfunc="mean"
    )

    median_close_apr = pd.pivot_table(
        subset,
        index="T0POTM_bucket",
        columns="T0APR_bucket",
        values="CloseAPR",
        aggfunc="median"
    )

    win_rate = pd.pivot_table(
        subset,
        index="T0POTM_bucket",
        columns="T0APR_bucket",
        values="Win",
        aggfunc="mean"
    ) * 100

    trade_count = pd.pivot_table(
        subset,
        index="T0POTM_bucket",
        columns="T0APR_bucket",
        values="TradeSequenceUUID",
        aggfunc="count"
    )

    avg_profit = pd.pivot_table(
        subset,
        index="T0POTM_bucket",
        columns="T0APR_bucket",
        values="TotalPremium",
        aggfunc="mean"
    )

    median_profit = pd.pivot_table(
        subset,
        index="T0POTM_bucket",
        columns="T0APR_bucket",
        values="TotalPremium",
        aggfunc="median"
    )

    # minimum trades threshold
    MIN_TRADES = 5

    # mask unreliable cells
    mask = trade_count < MIN_TRADES

    avg_close_apr = avg_close_apr.mask(mask)
    median_close_apr = median_close_apr.mask(mask)
    win_rate = win_rate.mask(mask)
    avg_profit = avg_profit.mask(mask)
    median_profit = median_profit.mask(mask)

    return {
        "avg_close_apr": avg_close_apr,
        "median_close_apr": median_close_apr,
        "win_rate": win_rate,
        "trade_count": trade_count,
        "avg_profit": avg_profit,
        "median_profit": median_profit,
    }

def find_best_zones(tables, min_trades=5):
    trade_count = tables["trade_count"]
    median_close_apr = tables["median_close_apr"]
    win_rate = tables["win_rate"]
    median_profit = tables["median_profit"]

    results = []

    for row in trade_count.index:
        for col in trade_count.columns:
            count = trade_count.loc[row, col]

            if pd.isna(count) or count < min_trades:
                continue

            results.append({
                "POTM": row,
                "APR": col,
                "Trades": int(count),
                "WinRate": win_rate.loc[row, col],
                "MedianCloseAPR": median_close_apr.loc[row, col],
                "MedianProfit": median_profit.loc[row, col],
            })

    result_df = pd.DataFrame(results)

    if result_df.empty:
        return result_df

    result_df = result_df.sort_values(
        by=["MedianCloseAPR", "WinRate"],
        ascending=False
    )

    return result_df