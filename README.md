# Engulfing Strategy Backtesting (Intraday)

This repository contains a **Python-based intraday backtesting framework** for an **Engulfing + Volume Confirmation** trading strategy.

The project focuses on:
- Clean signal generation
- Event-based trade execution
- Realistic position sizing
- Detailed P&L and transaction cost calculation
- Post-trade performance evaluation

The code is intentionally kept modular to allow further experimentation and extensions.

---

## Strategy Overview

The trading logic is based on:

1. **Engulfing Pattern Detection**
   - Bullish engulfing → potential long
   - Bearish engulfing → potential short

2. **Volume Confirmation**
   - Signal is considered only when volume is higher than a rolling volume average

3. **Event-Based Signals**
   - Signals are generated using **previous candle confirmation**
   - Avoids look-ahead bias

4. **Intraday Trading Constraints**
   - Trades are taken only within defined market hours
   - Supports time-based trade filtering

---

## Backtesting Logic

- One row per candle
- Signal → Entry → Exit flow
- Trades are executed only when:
  - Signal is present
  - Risk and position sizing conditions are satisfied
- Stop-loss and target are derived from candle structure and risk parameters

---

## Risk Management

- **Fixed monetary risk per trade**
- Quantity is calculated as:
- quantity = floor(monetary_risk / risk_in_points)

- Supports:
  - Risk–reward based exits
  - Optional reversal-based exit logic

---

## Transaction Costs Included

Realistic Indian market costs are modeled:

- Brokerage (capped)
- STT
- Exchange transaction charges
- SEBI charges
- GST
- Stamp duty

Net P&L is calculated **after all charges**.

---

## Performance Metrics

The framework computes:

- Trade-wise P&L
- Gross and net P&L
- Win rate and loss rate
- Average win and average loss
- Expectancy
- Drawdown
- MAE / MFE (planned / partially implemented)

---

## Project Structure

```text
engulfing_backtesting/
│
├── data/
│   └── Intraday OHLCV data (parquet)
│
├── backtest/
│   ├── signal.py            # Engulfing + volume signal logic
│   ├── execution.py         # Entry/exit handling
│   ├── position_sizing.py   # Quantity & risk logic
│   ├── costs.py             # Transaction cost calculation
│
├── analysis/
│   └── Performance metrics and diagnostics
│
├── notebooks/
│   └── Research & experimentation notebooks
│
├── main.py                  # End-to-end backtest runner
├── requirements.txt
└── README.md

