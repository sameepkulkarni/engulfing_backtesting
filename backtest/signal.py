# create volume moving average
def create_volume_moving_average(df, candles = 8):
  df = df.copy()
  df[f"vma_{candles}"] = df["volume"].rolling(window=candles).mean()  
  return df

# candle colour logic
def candlestick_colours(df):
  df = df.copy()
  df["candle"] = np.where(
    df["open"]>df["close"],"red", 
    np.where(df["open"]==df["close"],"white","green")
  )
  return df

# reversal logic
def reversal(df):
  df = df.copy()
  df["reversal"] = "None"
  bullish =( df["candle"].shift(1) == "red") & (df["candle"]=="green")
  bearish = (df["candle"].shift(1) == "green") & (df["candle"]=="red")
  df.loc[bullish, "reversal"] = "bullish"
  df.loc[bearish, "reversal"] = "bearish"
  return df

# englufing logic
def engulfing(df):
  df = df.copy()
  df["engulfing"] = "sluggish"
  bullish = (
      (df["reversal"] == "bullish") &
      (df["close"] > df["open"].shift(1)) & 
      (abs(df["close"] - df["open"])>=0.6 *abs(df["close"].shift(1) - df["open"].shift(1)))
  )
  bearish = (
      (df["reversal"] == "bearish") &
      (df["close"] < df["open"].shift(1)) & 
      (abs(df["close"] - df["open"])>=0.6 *abs(df["close"].shift(1) - df["open"].shift(1)))
  )
  df.loc[bullish, "engulfing"] = "bullish"
  df.loc[bearish, "engulfing"] = "bearish"
  return df

# volume check logic
def volume_check(df, candles=8):
  df = df.copy()
  df["volume_check"] = "lower"
  df.loc[df["volume"] > df[f"vma_{candles}"], "volume_check"] = "higher"
  return df

# signal logic
def signal(df ):
  df = df.copy()
  time_check = (df.index.time >= time(9,30) ) & (df.index.time <= time(14,40) )
  df["signal"] = 0
  long = time_check & (df["engulfing"].shift(1) == "bullish") & (df["volume_check"].shift(2) == "higher")
  short = time_check & (df["engulfing"].shift(1) == "bearish") & (df["volume_check"].shift(2) == "higher")
  df.loc[long, "signal"] = 1
  df.loc[short, "signal"] = -1
  return df
#entry logic
def entry(df):
  df = df.copy()
  df["entry_price"] = np.nan
  long = df["signal"] == 1
  short = df["signal"] == -1 
  df.loc[long | short, "entry_price"] = df["open"]
  return df

