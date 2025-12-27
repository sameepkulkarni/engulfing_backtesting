import numpy as np
import pandas as pd
from datetime import time

# trading simulation
def simulate_trade(df):
    df = df.copy()
    df["exit_reason"] = None
    df["exit_index"] = pd.NaT
    df["exit_price"] = np.nan

    trade_active_until = pd.NaT

    for i in range(len(df)):

      # block overlapping trades
      if pd.notna(trade_active_until) and df.index[i] <= trade_active_until:
          continue

      if df.iloc[i]["signal"] == 0:
          continue
      df.loc[df.index[i],'entry_time'] = df.index[i]
      sl = df.iloc[i]["stop_loss"]
      tp = df.iloc[i]["take_profit"]
      direction = df.iloc[i]["signal"]

      for j in range(i + 1, len(df)):
          high = df.iloc[j]["high"]
          low = df.iloc[j]["low"]
          open_price = df.iloc[j]["open"]
          signal = df.iloc[j]["signal"]

          if df.index[j].time() == time(15, 5):
              exit_reason, exit_price = "time_cutoff", open_price
              break

          if direction == 1:
              # if signal == -1:
              #     exit_reason, exit_price = "reversal", max(open_price, sl)
              #     break
              if low <= sl:
                  exit_reason, exit_price = "sl", sl
                  break
              if high >= tp:
                  exit_reason, exit_price = "tp", tp
                  break
          else:
              # if signal == 1:
              #     exit_reason, exit_price = "reversal", min(open_price, sl)
              #     break
              if high >= sl:
                  exit_reason, exit_price = "sl", sl
                  break
              if low <= tp:
                  exit_reason, exit_price = "tp", tp
                  break

      # record exit
      df.loc[df.index[i], ["exit_reason","exit_time","exit_price"]] = [exit_reason, df.index[j], exit_price]
      # lock until exit
      trade_active_until = df.index[j]

    return df

# post processing logic
def post_processing(df): 
  df = df.copy() 
  completed_trade = df['exit_time'].notna()
  df.loc[completed_trade,"pnl_points"] = (df.loc[completed_trade,"exit_price"] - df.loc[completed_trade,"entry_price"])* df.loc[completed_trade,"signal"] 
  df.loc[completed_trade,"monetary_pnl"] = df.loc[completed_trade,"pnl_points"] * df.loc[completed_trade,"quantity"] 
  df['net_pnl'] = df['monetary_pnl'] - df['total_costs']
  df["equity"] = df["net_pnl"].fillna(0).cumsum() 
  df["holding_time"] = df["exit_time"] - df["entry_time"]
  df["trade_direction"] = np.where(df["signal"]==1,"buy",np.where(df["signal"]==-1,"sell",""))
  df['drawdown'] = df['equity'].cummax() - df['equity']
  return df


# final results logic
def result(pnl):
  pnl = pnl.dropna()
  pnl = pnl[pnl!=0]
  wins = pnl[pnl>0]
  losses = pnl[pnl<0]
  avg_win = wins.mean()
  avg_loss = losses.mean()
  win_rate = len(wins)/len(pnl)
  loss_rate = len(losses)/len(pnl)
  expectancy = avg_win*win_rate+avg_loss*loss_rate
  drawdown = max(pnl.fillna(0).cumsum().cummax() - pnl.fillna(0).cumsum()) 
  return {
    "avg_win": avg_win,
    "avg_loss": avg_loss,
    "win_rate": win_rate,
    "loss_rate": loss_rate,
    "expectancy": expectancy,
    "drawdown": drawdown
  } 
  
# trades dataframe logic
def trades_df(df):
  df =df.copy()
  trades_df = df[['trade_direction','quantity','entry_time','exit_time','stop_loss','take_profit','risk_in_points','monetary_pnl','total_costs', 'net_pnl', 'holding_time','equity','drawdown']]
  trades_df = trades_df[trades_df['exit_time'].notna()]
  return trades_df