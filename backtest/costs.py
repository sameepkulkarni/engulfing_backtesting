import numpy as np
import pandas as pd

# transaction costs logic
def transaction_costs(df):
    df = df.copy()
    completed_trade = df['exit_time'].notna()
    # Turnover (buy + sell)
    df.loc[completed_trade, 'turnover'] = (
        (df.loc[completed_trade, 'entry_price'] + df.loc[completed_trade, 'exit_price'])
        * df.loc[completed_trade, 'quantity']
    )
    # Brokerage: 0.03% per side, capped at 20 per side
    brokerage_raw = 0.03/100 * df.loc[completed_trade, 'turnover'] / 2
    df.loc[completed_trade, 'brokerage'] = np.minimum(brokerage_raw, 20) * 2
    # STT: sell side only (intraday equity)
    df.loc[completed_trade, 'stt'] = (
        25/100000 * df.loc[completed_trade, 'exit_price'] * df.loc[completed_trade, 'quantity']
    )
    # Transaction charges
    df.loc[completed_trade, 'trans_charges'] = (
        0.00297/100 * df.loc[completed_trade, 'turnover']
    )
    # SEBI charges
    df.loc[completed_trade, 'sebi'] = (
        10/10000000 * df.loc[completed_trade, 'turnover']
    )
    # GST: only on brokerage + transaction charges
    df.loc[completed_trade, 'gst'] = (
        0.18 * (df.loc[completed_trade, 'brokerage'] + df.loc[completed_trade, 'trans_charges'])
    )
    # Stamp duty: buy side only
    df.loc[completed_trade, 'stamp_charges'] = (
        0.003/100 * df.loc[completed_trade, 'entry_price'] * df.loc[completed_trade, 'quantity']
    )

    # Total costs
    df.loc[completed_trade, 'total_costs'] = (
        df.loc[completed_trade, 'brokerage']
        + df.loc[completed_trade, 'stt']
        + df.loc[completed_trade, 'trans_charges']
        + df.loc[completed_trade, 'sebi']
        + df.loc[completed_trade, 'gst']
        + df.loc[completed_trade, 'stamp_charges']
    )

    return df