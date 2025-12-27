# load the file
def load_data(filename):
  return pd.read_parquet(filename)

# resample logic
def resample_ohlcv(df, timeframe):
  return (df.resample(timeframe, label="right", closed="right").agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
            "open_interest": "last"
        })
        .dropna(subset=["open"]))
