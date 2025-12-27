#import libraries
import numpy as np
import pandas as pd
import os
from datetime import time
import sys
from pathlib import Path

# Add project root to Python path
data_dir = Path.cwd() / "parquet_files"

from backtest.data import load_data, resample_ohlcv
from backtest.signal import create_volume_moving_average,candlestick_colours,reversal,engulfing, volume_check, signal, entry
from backtest.position_sizing import stop_loss, risk_in_points, take_profit, calc_quantity
from backtest.execution import simulate_trade, post_processing, trades_df
from backtest.costs import transaction_costs

first_test = os.path.join(data_dir, "RELIANCE.parquet")
reliance = load_data(first_test)
reliance = resample_ohlcv(reliance, "5min")
reliance = create_volume_moving_average(reliance, 8)
reliance = candlestick_colours(reliance)
reliance = reversal(reliance) 
reliance = engulfing(reliance)
reliance = volume_check(reliance, candles = 8)
reliance = signal(reliance)
reliance = entry(reliance)
reliance = stop_loss(reliance)
reliance = risk_in_points(reliance)
reliance = take_profit(reliance, rr = 2)
reliance = calc_quantity(reliance, monetary_risk=1000)
reliance = simulate_trade(reliance)
reliance = transaction_costs(reliance)
reliance = post_processing(reliance)
reliance.to_csv(r'analysis\whole_df.csv')
trades = trades_df(reliance)
trades.to_csv(r'analysis\trades.csv')