# src/strategies/mean_reversion.py

from .base import BaseStrategy
import pandas as pd

class MeanReversionStrategy(BaseStrategy):
    def __init__(self, window=20):
        super().__init__("MeanReversion")
        self.window = window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        # 範例邏輯
        close = data["close"]
        sma = close.rolling(window=self.window).mean()
        signals = ["HOLD"]
        for i in range(1, len(data)):
            if close[i] < sma[i]:
                signals.append("BUY")
            else:
                signals.append("HOLD")
        return pd.Series(signals)