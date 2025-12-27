
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

