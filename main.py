#import libraries
import numpy as np
import pandas as pd
import os
from datetime import time
import sys
from pathlib import Path
data_dir = Path.cwd() / "parquet_files"

from backtest.data import load_data, resample_ohlcv
from backtest.signal import create_volume_moving_average,candlestick_colours,reversal,engulfing, volume_check, signal, entry
from backtest.position_sizing import stop_loss, risk_in_points, take_profit, calc_quantity
from backtest.execution import simulate_trade, post_processing, trades_df, result
from backtest.costs import transaction_costs
from backtest.config import rr, lookback_window, resample_timeframe, monetary_risk

first_test = os.path.join(data_dir, "RELIANCE.parquet")
reliance = load_data(first_test)
reliance = resample_ohlcv(reliance, resample_timeframe)
reliance = create_volume_moving_average(reliance, lookback_window)
reliance = candlestick_colours(reliance)
reliance = reversal(reliance) 
reliance = engulfing(reliance)
reliance = volume_check(reliance, candles = lookback_window)
reliance = signal(reliance)
reliance = entry(reliance)
reliance = stop_loss(reliance)
reliance = risk_in_points(reliance)
reliance = take_profit(reliance, rr = rr)
reliance = calc_quantity(reliance, monetary_risk= monetary_risk)
reliance = simulate_trade(reliance)
reliance = transaction_costs(reliance)
reliance = post_processing(reliance)
reliance.to_csv(r'analysis\whole_df.csv')
trades = trades_df(reliance)
trades.to_csv(r'analysis\trades.csv')
results = result(reliance['net_pnl'])
results = pd.DataFrame([results])
results.to_csv(r'analysis\result.csv')