"""
SOXL Put - Median Close APR Heatmap

This visualization shows how different trade entry conditions (T0 APR and T0 % Out-Of-The-Money)
translate into final performance outcomes, measured by Median Close APR.

Each cell represents a group of trades that share similar:
- Initial APR at trade open (T0APR)
- Initial distance from the strike price (T0POTM)

The value in each cell is the median Close APR of those trades, which reflects the actual
annualized return achieved after the trade is closed.

This heatmap answers the question:
"What combinations of initial APR and POTM tend to produce the best returns?"

Higher values (green) indicate stronger performance, while lower values (red) indicate weaker outcomes.
Gray cells indicate insufficient data.

This is a performance-focused view and does not account for how often trades succeed or how frequently
these conditions occur.
"""
from data_loader import load_pickle_file
from analytics import calculate_trade_summary
from strategy_heatmap_analysis import add_analysis_buckets, build_heatmap_tables

import matplotlib.pyplot as plt
import numpy as np

def make_soxl_put_median_close_apr_heatmap():
    data = load_pickle_file("data/test_data.pkl")
    summary = calculate_trade_summary(data)
    analysis_df = add_analysis_buckets(summary)

    tables = build_heatmap_tables(analysis_df, "SOXL", "Put")
    heatmap_data = tables["median_close_apr"].copy()

    # Keep row/column order stable
    heatmap_data = heatmap_data.sort_index()

    # Build figure
    fig, ax = plt.subplots(figsize=(12, 7))

    # mask NaN values so they show as gray instead of red
    masked_data = np.ma.masked_invalid(heatmap_data.values)

    cmap = plt.cm.RdYlGn.copy()
    cmap.set_bad(color="lightgray")

    image = ax.imshow(
        masked_data,
        aspect="auto",
        cmap=cmap
    )

    # Axis labels
    ax.set_title("SOXL Put - Median Close APR Heatmap")
    ax.set_xlabel("T0 APR Bucket")
    ax.set_ylabel("T0 POTM Bucket")

    # Tick labels
    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")

    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)

    # Annotate each cell
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            value = heatmap_data.iloc[i, j]

            if value != value:  # NaN check
                text = "N/A"
            else:
                text = f"{value:.1f}"

            ax.text(j, i, text, ha="center", va="center", fontsize=8)

    # Colorbar
    fig.colorbar(image, ax=ax, label="Median Close APR")

    plt.tight_layout()
    plt.savefig("data/SOXL_put_median_close_apr_heatmap.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    make_soxl_put_median_close_apr_heatmap()