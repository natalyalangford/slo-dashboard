"""
SOXL Put - Win Rate Heatmap

This visualization shows how often trades are profitable based on their initial conditions
(T0 APR and T0 % Out-Of-The-Money).

Each cell represents a group of trades with similar:
- Initial APR at trade open (T0APR)
- Initial distance from the strike price (T0POTM)

The value in each cell is the percentage of trades in that group that resulted in a positive outcome
(i.e., TotalPremium > 0).

This heatmap answers the question:
"How reliable is a given strategy in terms of winning trades?"

Higher values (green) indicate more consistent success, while lower values (red) indicate
greater risk of losing trades. Gray cells indicate insufficient data.

This is a consistency-focused view and should be interpreted alongside performance (Close APR),
since a high win rate does not necessarily imply high returns.
"""
from data_loader import load_pickle_file
from analytics import calculate_trade_summary
from strategy_heatmap_analysis import add_analysis_buckets, build_heatmap_tables
import numpy as np
import matplotlib.pyplot as plt


def make_soxl_put_winrate_heatmap():
    data = load_pickle_file("data/test_data.pkl")
    summary = calculate_trade_summary(data)
    analysis_df = add_analysis_buckets(summary)

    tables = build_heatmap_tables(analysis_df, "SOXL", "Put")
    heatmap_data = tables["win_rate"].copy()

    heatmap_data = heatmap_data.sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))

    # mask NaN values so they show as gray instead of red
    masked_data = np.ma.masked_invalid(heatmap_data.values)

    cmap = plt.cm.RdYlGn.copy()
    cmap.set_bad(color="lightgray")

    image = ax.imshow(
        masked_data,
        aspect="auto",
        cmap=cmap
    )

    ax.set_title("SOXL Put - Win Rate Heatmap")
    ax.set_xlabel("T0 APR Bucket")
    ax.set_ylabel("T0 POTM Bucket")

    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")

    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)

    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            value = heatmap_data.iloc[i, j]

            if value != value:
                text = "N/A"
            else:
                text = f"{value:.1f}%"

            ax.text(j, i, text, ha="center", va="center", fontsize=8)

    fig.colorbar(image, ax=ax, label="Win Rate (%)")

    plt.tight_layout()
    plt.savefig("data/SOXL_put_winrate_heatmap.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    make_soxl_put_winrate_heatmap()