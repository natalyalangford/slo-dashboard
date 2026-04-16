"""
SOXL Put - Trade Count Heatmap

This visualization shows how many trades exist for each combination of initial conditions
(T0 APR and T0 % Out-Of-The-Money).

Each cell represents a group of trades with similar:
- Initial APR at trade open (T0APR)
- Initial distance from the strike price (T0POTM)

The value in each cell is the total number of trades observed in that group.

This heatmap answers the question:
"How often do these types of trades actually occur?"

Higher values (darker blue) indicate more frequent and statistically reliable trade patterns,
while lower values indicate sparse data that may not be reliable for decision-making.
Gray cells indicate no data.

This is a frequency and data reliability view, and it is critical for validating insights from
the performance and win rate heatmaps.
"""
from data_loader import load_pickle_file
from analytics import calculate_trade_summary
from strategy_heatmap_analysis import add_analysis_buckets, build_heatmap_tables

import matplotlib.pyplot as plt
import numpy as np


def make_soxl_put_tradecount_heatmap():
    data = load_pickle_file("data/test_data.pkl")
    summary = calculate_trade_summary(data)
    analysis_df = add_analysis_buckets(summary)

    tables = build_heatmap_tables(analysis_df, "SOXL", "Put")
    heatmap_data = tables["trade_count"].copy()

    heatmap_data = heatmap_data.sort_index()

    # mask NaN values
    masked_data = np.ma.masked_invalid(heatmap_data.values)

    cmap = plt.cm.Blues.copy()  # use blue scale for counts
    cmap.set_bad(color="lightgray")

    fig, ax = plt.subplots(figsize=(10, 6))

    image = ax.imshow(
        masked_data,
        aspect="auto",
        cmap=cmap
    )

    ax.set_title("SOXL Put - Trade Count Heatmap")
    ax.set_xlabel("T0 APR Bucket")
    ax.set_ylabel("T0 POTM Bucket")

    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")

    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)

    # annotate cells
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            value = heatmap_data.iloc[i, j]

            if value != value:  # NaN
                text = "N/A"
            else:
                text = f"{int(value)}"

            ax.text(j, i, text, ha="center", va="center", fontsize=9)

    fig.colorbar(image, ax=ax, label="Trade Count")

    plt.tight_layout()
    plt.savefig("data/SOXL_put_tradecount_heatmap.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    make_soxl_put_tradecount_heatmap()