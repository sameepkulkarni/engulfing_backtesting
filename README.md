# Engulfing Strategy — Intraday Research Framework

This repository is an **ongoing quantitative research project** focused on studying the
**viability, stability, and risk characteristics** of intraday price-action strategies,
starting with an **Engulfing + Volume confirmation** setup.

The objective is **not** to present a finished or profitable trading system, but to build
a **research-grade backtesting framework** that allows systematic experimentation with
signals, execution rules, risk controls, and exit logic.

---

## Research Motivation

Simple candlestick patterns often appear statistically attractive in isolation but tend
to degrade once realistic execution constraints and risk controls are applied.

This project investigates:
- When (and if) engulfing patterns have predictive value
- How expectancy changes with different exits and risk rules
- The trade-off between **expectancy improvement and drawdown expansion**
- Whether signal quality or risk control contributes more to long-term stability

---

## Current Scope (Implemented So Far)

The current implementation establishes a **clean experimental baseline**.

### 1. Signal Generation
- Bullish and bearish engulfing pattern detection
- Volume confirmation using rolling volume averages
- **Previous-candle confirmation** to avoid look-ahead bias
- Event-based signal generation (not indicator repainting)

### 2. Execution & Position Sizing
- Intraday trade execution model
- Fixed monetary risk per trade
- Quantity calculated from stop-loss distance
- Candle-structure-based SL and RR-based targets

### 3. Transaction Cost Modeling
Realistic Indian market costs are applied:
- Brokerage (with cap)
- STT
- Exchange transaction charges
- SEBI charges
- GST
- Stamp duty

All reported P&L is **net of costs**.

### 4. Performance Measurement
- Trade-wise P&L
- Win rate and loss rate
- Average win / average loss
- Expectancy
- Equity curve and drawdown tracking

---

## Known Limitations (Explicitly Acknowledged)

This project is **intentionally incomplete**.

Currently missing or only partially implemented:
- MAE / MFE distribution analysis
- Parameter stability and sensitivity testing
- Regime segmentation (volatility, trend)
- Robust trade frequency control
- Walk-forward or out-of-sample validation

No claim of robustness or profitability is made at this stage.

---

## Research Roadmap (Planned Work)

The following areas will be incorporated incrementally.

### 1. Signal Quality Research
- Variants of engulfing definitions
- Relative vs normalized volume filters
- Time-of-day filters
- Volatility-conditioned signal filtering

### 2. Trade Frequency Control
- One-trade-per-day vs multiple-trade regimes
- Cool-down logic after consecutive losses
- Signal clustering suppression

### 3. Exit Logic Experiments
- Fixed RR vs adaptive RR
- Reversal-based exits
- Time-based exits
- Partial exits and scale-outs

### 4. Risk & Drawdown Control
- Daily loss limits
- Max consecutive loss rules
- Equity-curve-aware risk scaling
- Volatility-adjusted position sizing

### 5. Post-Trade Diagnostics (Critical)
- MAE / MFE distributions
- Expectancy vs drawdown heatmaps
- Tail-loss and adverse excursion analysis
- Trade duration analysis

### 6. Robustness & Bias Checks
- Look-ahead and survivorship bias validation
- Parameter sensitivity stress testing
- Basic walk-forward testing

---

## Project Philosophy

This repository follows a **research-first approach**:

- No curve-fitting for isolated metrics
- Preference for **expectancy stability over peak returns**
- Drawdown behavior treated as a first-class metric
- Explicit acknowledgment of uncertainty and limitations

The framework is designed to evolve as research questions become sharper.

---

## Intended Use

- Quantitative research practice
- Strategy development experimentation
- Learning systematic trading design
- Foundation for more advanced market-structure-based strategies

---

## Disclaimer

This project is strictly for **research and educational purposes**.
It is **not intended for live trading** or investment advice.

---

## Author

**Sameep Kulkarni**  
Risk Management | Quantitative Research | Algorithmic Trading
