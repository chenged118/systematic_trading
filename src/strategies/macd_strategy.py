# src/strategies/macd_strategy.py

import pandas as pd
from .base import BaseStrategy

class MACDStrategy(BaseStrategy):
    def __init__(self, fast=12, slow=26, signal=9):
        super().__init__("MACD")
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        close = data["close"]
        ema_fast = close.ewm(span=self.fast, adjust=False).mean()
        ema_slow = close.ewm(span=self.slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=self.signal, adjust=False).mean()

        # MACD crossover strategy
        signals = []
        for i in range(len(macd)):
            if i == 0:
                signals.append("HOLD")
            elif macd[i - 1] < signal_line[i - 1] and macd[i] > signal_line[i]:
                signals.append("BUY")
            elif macd[i - 1] > signal_line[i - 1] and macd[i] < signal_line[i]:
                signals.append("SELL")
            else:
                signals.append("HOLD")
        return pd.Series(signals)