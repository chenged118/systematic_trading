# src/backtest/engine.py

import pandas as pd
from src.strategies.base import BaseStrategy
from src.strategies import get_strategy

class CompositeStrategy(BaseStrategy):
    def __init__(self, strategy_list):
        super().__init__("Composite")
        self.strategies = strategy_list

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        all_signals = [s.generate_signals(data) for s in self.strategies]
        return self.aggregate_votes(all_signals)

    def aggregate_votes(self, vote_series_list: list[pd.Series]) -> pd.Series:
        final = []
        for i in range(len(vote_series_list[0])):
            votes = [v[i] for v in vote_series_list]
            if votes.count("BUY") > votes.count("SELL"):
                final.append("BUY")
            elif votes.count("SELL") > votes.count("BUY"):
                final.append("SELL")
            else:
                final.append("HOLD")
        return pd.Series(final)

def run_backtest(data: pd.DataFrame, strategy: BaseStrategy):
    signals = strategy.generate_signals(data)
    print("📈 模擬交易訊號（前 10 筆）:")
    print(signals.head(10))
    # 可擴充為下單模擬、績效計算等