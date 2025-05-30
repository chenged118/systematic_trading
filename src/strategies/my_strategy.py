# src/strategies/my_strategy.py

import pandas as pd
from .base import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self, short_window=5, long_window=20):
        super().__init__(name="my")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        data = data.copy()
        data['sma_short'] = data['close'].rolling(window=self.short_window).mean()
        data['sma_long'] = data['close'].rolling(window=self.long_window).mean()

        signals = ['HOLD'] * len(data)

        for i in range(1, len(data)):
            if data['sma_short'].iloc[i] > data['sma_long'].iloc[i] and \
               data['sma_short'].iloc[i-1] <= data['sma_long'].iloc[i-1]:
                signals[i] = 'BUY'
            elif data['sma_short'].iloc[i] < data['sma_long'].iloc[i] and \
                 data['sma_short'].iloc[i-1] >= data['sma_long'].iloc[i-1]:
                signals[i] = 'SELL'
        
        return pd.Series(signals, index=data.index)