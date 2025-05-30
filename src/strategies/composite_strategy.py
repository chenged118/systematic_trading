# src/strategies/composite_strategy.py

import pandas as pd
from .base import BaseStrategy

class CompositeStrategy(BaseStrategy):
    def __init__(self, strategies: list):
        super().__init__("Composite")
        self.strategies = strategies

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        # 範例：每個策略票選，BUY > HOLD > SELL
        votes = [s.generate_signals(data) for s in self.strategies]
        return self.aggregate_votes(votes)

    def aggregate_votes(self, votes: list[pd.Series]) -> pd.Series:
        result = []
        for i in range(len(votes[0])):
            vote_count = [v[i] for v in votes]
            if vote_count.count('BUY') > vote_count.count('SELL'):
                result.append('BUY')
            elif vote_count.count('SELL') > vote_count.count('BUY'):
                result.append('SELL')
            else:
                result.append('HOLD')
        return pd.Series(result)