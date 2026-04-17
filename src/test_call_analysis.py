from data_loader import load_pickle_file
from analytics import calculate_trade_summary
from call_analysis import (
    analyze_calls,
    analyze_calls_by_potm,
    find_best_call_zones,
    find_worst_call_zones,
    get_potm_distribution
)


def print_metric_block(title, metrics):
    print(f"\n{title}")
    print("-" * len(title))
    if metrics is None:
        print("No data available.")
        return

    for key, value in metrics.items():
        print(f"{key}: {value}")


def main():
    data = load_pickle_file("data/test_data.pkl")
    summary = calculate_trade_summary(data)

    print("\nCALL POTM DISTRIBUTION - ALL CALLS")
    dist_all = get_potm_distribution(summary)
    print(dist_all.to_string(index=False))

    print("\nCALL POTM DISTRIBUTION - AMD ONLY")
    dist_amd = get_potm_distribution(summary, stocks=["AMD"])
    print(dist_amd.to_string(index=False))

    # All calls
    overall = analyze_calls(summary)
    print_metric_block("CALL STRATEGY ANALYSIS - ALL CALLS", overall)

    # AMD-only calls
    amd_calls = analyze_calls(summary, stocks=["AMD"])
    print_metric_block("CALL STRATEGY ANALYSIS - AMD ONLY", amd_calls)

    # Calls by POTM for all calls
    all_potm = analyze_calls_by_potm(summary)
    print("\nCALL ANALYSIS BY POTM - ALL CALLS")
    print(all_potm.to_string(index=False))

    # Calls by POTM for AMD only
    amd_potm = analyze_calls_by_potm(summary, stocks=["AMD"])
    print("\nCALL ANALYSIS BY POTM - AMD ONLY")
    print(amd_potm.to_string(index=False))

    best_zones = find_best_call_zones(amd_potm, min_trades=5)
    worst_zones = find_worst_call_zones(amd_potm, min_trades=5)

    print("\nBEST AMD CALL ZONES")
    if best_zones.empty:
        print("No zones with enough trades.")
    else:
        print(best_zones.head(10).to_string(index=False))
        best_zones.to_csv("data/AMD_call_best_zones.csv", index=False)
        print("\nSaved to data/AMD_call_best_zones.csv")

    print("\nWORST AMD CALL ZONES")
    if worst_zones.empty:
        print("No zones with enough trades.")
    else:
        print(worst_zones.head(10).to_string(index=False))
        worst_zones.to_csv("data/AMD_call_worst_zones.csv", index=False)
        print("\nSaved to data/AMD_call_worst_zones.csv")

    amd_potm.to_csv("data/AMD_call_analysis_by_potm.csv", index=False)
    print("\nSaved to data/AMD_call_analysis_by_potm.csv")

    call_summary = summary[summary["Type"] == "Call"].copy()
    call_summary.to_csv("data/call_trade_summary.csv", index=False)
    print("\nSaved to data/call_trade_summary.csv")

if __name__ == "__main__":
    main()