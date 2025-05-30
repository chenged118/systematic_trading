# src/strategies/breakout.py

from .base import BaseStrategy
import pandas as pd

class BreakoutStrategy(BaseStrategy):
    def __init__(self, lookback=20):
        super().__init__("Breakout")
        self.lookback = lookback

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        signals = []
        for i in range(len(data)):
            if i < self.lookback:
                signals.append("HOLD")
            elif data["close"][i] > max(data["close"][i-self.lookback:i]):
                signals.append("BUY")
            else:
                signals.append("HOLD")
        return pd.Series(signals)