# sl logic
def stop_loss(df):
  df = df.copy()
  df["stop_loss"] = 0.0
  long = df["signal"] == 1
  short = df["signal"] == -1 
  df.loc[long, "stop_loss"] = df["low"].shift(1).rolling(2).min()
  df.loc[short, "stop_loss"] = df["high"].shift(1).rolling(2).max()
  return df

# risk in points logic 
def risk_in_points(df):
  df = df.copy()
  df["risk_in_points"]= np.nan 
  signal_present = (df["signal"] == 1) | (df["signal"] == -1)
  df.loc[signal_present, "risk_in_points"] = (df["open"] - df["stop_loss"])*(df["signal"])
  return df 

#exit logic
def take_profit(df,rr= 2):
  df = df.copy()
  df["take_profit"] = np.nan
  long = df["signal"] == 1
  short = df["signal"] == -1 
  df.loc[long, "take_profit"] = df["risk_in_points"]*rr + df["open"]
  df.loc[short, "take_profit"] = df["open"] - df["risk_in_points"]*rr
  return df

# quantity logic
def calc_quantity(df, monetary_risk = 1000):
  df = df.copy()
  df["quantity"] = 0.0
  signal_present = (df["signal"] == 1) | (df["signal"] == -1)
  df.loc[signal_present, "quantity"] = np.floor(monetary_risk / df.loc[signal_present, "risk_in_points"])
  return df