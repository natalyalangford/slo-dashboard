from data_loader import load_pickle_file
from analytics import calculate_trade_summary
from strategy_heatmap_analysis import (
    add_analysis_buckets,
    build_heatmap_tables,
    find_best_zones,
)


def main():
    data = load_pickle_file("data/test_data.pkl")
    summary = calculate_trade_summary(data)
    analysis_df = add_analysis_buckets(summary)

    print("\nStocks in dataset:")
    print(data["Stock"].value_counts())

    groups = [
        ("SOXL", "Put"),
        ("SOXL", "Call"),
        ("TQQQ", "Put"),
        ("TQQQ", "Call"),
    ]

    for stock, option_type in groups:
        print("\n==============================")
        print(f"{stock} {option_type}")
        print("==============================")

        tables = build_heatmap_tables(analysis_df, stock, option_type)

        print("\nTrade Count")
        print(tables["trade_count"].fillna(0).to_string())

        print("\nWin Rate (%)")
        print(tables["win_rate"].round(2).fillna(0).to_string())

        print("\nAverage Close APR")
        print(tables["avg_close_apr"].round(2).fillna(0).to_string())

        print("\nMedian Close APR")
        print(tables["median_close_apr"].round(2).fillna(0).to_string())

        print("\nAverage Profit")
        print(tables["avg_profit"].round(2).fillna(0).to_string())

        print("\nMedian Profit")
        print(tables["median_profit"].round(2).fillna(0).to_string())

        best_zones = find_best_zones(tables)

        print("\nBEST ZONES")
        if best_zones.empty:
            print("No zones with enough trades.")
        else:
            print(best_zones.head(10).to_string(index=False))
            best_zones.to_csv(f"data/{stock}_{option_type}_best_zones.csv", index=False)
            print(f"\nSaved to data/{stock}_{option_type}_best_zones.csv")


if __name__ == "__main__":
    main()