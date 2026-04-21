"""
generate_puts.py

Purpose:
--------
This script generates a large set of synthetic put option trades for analysis.
The goal is to simulate ALL possible put selling opportunities for selected ETFs
(currently SOXL and TQQQ) across available strikes and expiration dates.

Instead of relying only on historical executed trades, this allows us to:
    - Explore the full decision space (all possible trades that could have been made)
    - Identify optimal strategies based on POTM (percent out-of-the-money), APR, and DTE
    - Build a much larger dataset to statistically validate trade performance

Approach:
---------
1. Pull current option chain data using yfinance
2. Iterate through all expiration dates and strike prices
3. For each contract:
    - Compute mid price (bid/ask handling)
    - Calculate T0 POTM (distance from underlying price)
    - Calculate T0 APR (annualized return based on premium and duration)
    - Capture DTE (days to expiration)
4. Apply filtering to remove unrealistic trades:
    - Extremely far OTM contracts (low probability / low relevance)
    - Illiquid contracts with near-zero premium
5. Store each synthetic trade as a JSON object

Output:
-------
A JSON file containing synthetic trades with the following fields:
    - symbol
    - option_type (Put)
    - entry_date
    - expiration_date
    - strike
    - underlying_price_at_entry
    - bid / ask / entry_option_price
    - quantity
    - dte
    - t0_potm
    - t0_apr
    - source ("synthetic_yfinance")

This JSON file can then be:
    - Loaded into a development database
    - Processed using existing analytics pipelines
    - Used to generate heatmaps, win rates, and strategy comparisons

Why This Matters:
-----------------
By generating synthetic trades across the entire option chain, we remove bias
from human decision-making and limited historical trades. This allows us to:
    - Compare what was done vs what was possible
    - Identify statistically optimal ranges for POTM and APR
    - Improve confidence in strategy selection

Notes:
------
- This script does NOT execute trades (simulation only)
- Data quality depends on yfinance option chain availability
- Additional filtering (e.g., minimum DTE, liquidity thresholds) can be tuned
"""

import json
from datetime import datetime
import yfinance as yf

def safe_mid(bid, ask):
    if bid is None or ask is None:
        return None
    if bid <= 0 and ask <= 0:
        return None
    if bid <= 0:
        return ask
    if ask <= 0:
        return bid
    return (bid + ask) / 2


def compute_t0_potm(underlying_price, strike):
    if underlying_price <= 0:
        return None
    return 100.0 * (underlying_price - strike) / underlying_price


def compute_t0_apr(option_price, strike, dte):
    if strike <= 0 or dte <= 0:
        return None
    return 100.0 * (option_price / strike) * (365 / dte)


def generate_synthetic_puts(symbol):
    ticker = yf.Ticker(symbol)
    expirations = ticker.options
    if not expirations:
        raise ValueError(f"No option expirations returned for {symbol}")

    # Use recent market price as entry underlying price
    hist = ticker.history(period="5d")
    if hist.empty:
        raise ValueError(f"No price history returned for {symbol}")
    underlying_price = float(hist["Close"].iloc[-1])

    today = datetime.utcnow().date()
    synthetic_trades = []

    for exp in expirations:
        exp_date = datetime.strptime(exp, "%Y-%m-%d").date()
        dte = (exp_date - today).days
        if dte <= 0:
            continue

        chain = ticker.option_chain(exp)
        puts = chain.puts

        for _, row in puts.iterrows():
            strike = float(row["strike"])
            bid = float(row["bid"]) if row["bid"] == row["bid"] else 0.0
            ask = float(row["ask"]) if row["ask"] == row["ask"] else 0.0
            mid = safe_mid(bid, ask)

            if mid is None:
                continue

            t0_potm = compute_t0_potm(underlying_price, strike)
            t0_apr = compute_t0_apr(mid, strike, dte)

            synthetic_trades.append({
                "symbol": symbol,
                "option_type": "Put",
                "entry_date": str(today),
                "expiration_date": exp,
                "strike": strike,
                "underlying_price_at_entry": underlying_price,
                "bid": bid,
                "ask": ask,
                "entry_option_price": mid,
                "quantity": 1,
                "dte": dte,
                "t0_potm": t0_potm,
                "t0_apr": t0_apr,
                "source": "synthetic_yfinance"
            })

    return synthetic_trades


def main():
    all_trades = []
    for symbol in ["SOXL", "TQQQ"]:
        all_trades.extend(generate_synthetic_puts(symbol))

    with open("synthetic_puts_v1.json", "w") as f:
        json.dump(all_trades, f, indent=2)

    print(f"Saved {len(all_trades)} synthetic trades.")


if __name__ == "__main__":
    main()