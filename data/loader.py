# src/data/loader.py

import pandas as pd

def load_market_data(path: str):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df