from data_loader import load_pickle_file
from analytics import calculate_trade_summary
from metrics import calculate_metrics
from bucket_analysis import analyze_potm_buckets


def main():
    data = load_pickle_file("data/slo_trades_29dec25.pkl")

    summary = calculate_trade_summary(data)

    print(summary.head())
    print("\nTotal trades:", len(summary))

    metrics = calculate_metrics(summary)

    print("\n--- Metrics ---")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    bucket_results = analyze_potm_buckets(summary)

    print("\n--- POTM Bucket Analysis ---")
    print(bucket_results.to_string(index=False))

    bucket_results.to_csv("data/potm_bucket_analysis.csv", index=False)
    print("\nSaved to data/potm_bucket_analysis.csv")

    print("\n--- Sample Strategy Columns ---")
    print(summary[[
        "Stock", "Type", "TotalPremium", "T0POTM", "T0APR"
    ]].head())

    summary.to_csv("data/trade_summary.csv", index=False)
    print("\nSaved to data/trade_summary.csv")


if __name__ == "__main__":
    main()