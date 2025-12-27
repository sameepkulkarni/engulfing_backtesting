# quantity logic
def calc_quantity(df, monetary_risk = 1000):
  df = df.copy()
  df["quantity"] = 0.0
  signal_present = (df["signal"] == 1) | (df["signal"] == -1)
  df.loc[signal_present, "quantity"] = np.floor(monetary_risk / df.loc[signal_present, "risk_in_points"])
  return df