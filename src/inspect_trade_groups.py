from data_loader import load_pickle_file


def main():
    file_path = "data/slo_trades_29dec25.pkl"
    data = load_pickle_file(file_path)

    sample_id = data["TradeSequenceUUID"].iloc[0]
    trade_rows = data[data["TradeSequenceUUID"] == sample_id].copy()

    trade_rows = trade_rows.sort_values("ExecutionDatetime")

    columns_to_show = [
        "TradeSequenceUUID",
        "Symbol",
        "Stock",
        "Type",
        "Status",
        "Position",
        "Cover",
        "StrikePrice",
        "Premium",
        "Price",
        "Quantity",
        "FeesAndCommission",
        "ExecutionDatetime",
        "ExecutionQuote",
    ]

    print(trade_rows[columns_to_show].to_string(index=False))

    print("\nUnique Position values:")
    print(sorted(data["Position"].dropna().unique()))

    print("\nUnique Status values:")
    print(sorted(data["Status"].dropna().unique()))

    print("\nUnique Type values:")
    print(sorted(data["Type"].dropna().unique()))

    print("\nUnique Cover values:")
    print(sorted(data["Cover"].dropna().unique()))


if __name__ == "__main__":
    main()