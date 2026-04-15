from data_loader import load_pickle_file


def main():
    file_path = "data/slo_trades_29dec25.pkl"
    data = load_pickle_file(file_path)

    print("Loaded successfully.")
    print("Type of data:", type(data))

    if hasattr(data, "shape"):
        print("Shape:", data.shape)

    if hasattr(data, "columns"):
        print("Columns:")
        for column in data.columns:
            print("-", column)

    print("\nPreview:")
    try:
        print(data.head())
    except AttributeError:
        print(data)

    if isinstance(data, dict):
        print("\nDictionary keys:")
        for key in data.keys():
            print("-", key)

    if isinstance(data, list) and len(data) > 0:
        print("\nFirst item in list:")
        print(data[0])

    if hasattr(data, "dtypes"):
        print("\nData types:")
        print(data.dtypes)

    if hasattr(data, "isnull"):
        print("\nMissing values:")
        print(data.isnull().sum())

    if "TradeSequenceUUID" in data.columns:
        print("\n--- Trade Group Analysis ---")
        total_rows = len(data)
        unique_trades = data["TradeSequenceUUID"].nunique()

        print("Total rows:", total_rows)
        print("Unique trades:", unique_trades)
        print("Average rows per trade:", total_rows / unique_trades)

        sample_id = data["TradeSequenceUUID"].iloc[0]
        print("\nSample TradeSequenceUUID:", sample_id)
        print(data[data["TradeSequenceUUID"] == sample_id])


if __name__ == "__main__":
    main()