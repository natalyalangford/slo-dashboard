# Options Strategy Analysis Dashboard (SOXL / TQQQ)

## Overview
This project analyzes options trading strategies by evaluating how trade entry conditions
impact final outcomes. The goal is to identify patterns that maximize return while managing risk.

The analysis focuses on:
- T0 APR (initial annualized return at trade open)
- T0 % Out-Of-The-Money (distance from strike price)
- Final trade outcomes (profitability and realized APR)

---

## Analysis Framework

Each strategy is evaluated across three dimensions:

1. **Close APR (Performance)**
   - Measures the actual annualized return after a trade closes
   - Answers: *How profitable is this strategy?*

2. **Win Rate (Consistency)**
   - Measures how often trades are profitable
   - Answers: *How reliable is this strategy?*

3. **Trade Count (Frequency / Reliability)**
   - Measures how often these conditions occur in historical data
   - Answers: *Is this strategy repeatable?*

A strong strategy balances all three:
- High returns
- High consistency
- Sufficient trade volume

---

## Key Findings (SOXL Puts)

- **Optimal Strategy:**
  - 5–10% Out-Of-The-Money
  - High T0 APR (80%+)
  - Strong balance of return (~110% APR), consistency (~75% win rate), and frequency

- **Safe Strategy:**
  - 15%+ Out-Of-The-Money
  - Moderate APR (40–80)
  - High win rate (80–95%), lower but stable returns

- **Aggressive Strategy:**
  - 0–5% Out-Of-The-Money
  - High APR (80%+)
  - High returns but lower consistency

---

## Purpose

This analysis is used to:
- Validate trading strategies using historical data
- Identify optimal trade setups
- Provide a foundation for future dashboard visualization and decision support tools