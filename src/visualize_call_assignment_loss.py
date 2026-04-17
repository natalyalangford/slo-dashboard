from data_loader import load_pickle_file
from analytics import calculate_trade_summary
from call_analysis import analyze_calls_by_potm

import matplotlib.pyplot as plt


def plot_call_loss_by_potm(potm_df, column_name, title, ylabel, output_file):
    df = potm_df.copy()
    df = df[df["TradeCount"] > 0].copy()

    x = df["POTM_bucket"].astype(str)
    y = df[column_name]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(x, y)

    ax.set_title(title)
    ax.set_xlabel("T0 POTM Bucket")
    ax.set_ylabel(ylabel)

    for bar, value in zip(bars, y):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.0f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.show()


def make_call_loss_charts():
    data = load_pickle_file("data/test_data.pkl")
    summary = calculate_trade_summary(data)

    # -------------------------
    # ALL CALLS
    # -------------------------
    all_potm = analyze_calls_by_potm(summary)

    plot_call_loss_by_potm(
        all_potm,
        "AvgCombinedLoss",
        "All Calls - Average Combined Loss by T0 POTM",
        "Average Combined Loss ($)",
        "data/all_calls_avg_combined_loss.png"
    )

    plot_call_loss_by_potm(
        all_potm,
        "MaxCombinedLoss",
        "All Calls - Max Combined Loss by T0 POTM",
        "Max Combined Loss ($)",
        "data/all_calls_max_combined_loss.png"
    )

    # -------------------------
    # AMD ONLY
    # -------------------------
    amd_potm = analyze_calls_by_potm(summary, stocks=["AMD"])

    plot_call_loss_by_potm(
        amd_potm,
        "AvgCombinedLoss",
        "AMD Calls - Average Combined Loss by T0 POTM",
        "Average Combined Loss ($)",
        "data/amd_calls_avg_combined_loss.png"
    )

    plot_call_loss_by_potm(
        amd_potm,
        "MaxCombinedLoss",
        "AMD Calls - Max Combined Loss by T0 POTM",
        "Max Combined Loss ($)",
        "data/amd_calls_max_combined_loss.png"
    )


if __name__ == "__main__":
    make_call_loss_charts()