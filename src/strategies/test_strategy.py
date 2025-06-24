# src/strategies/test_strategy.py

import pandas as pd
from .base import BaseStrategy

class TestStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="test")
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        print(f"[{self.name}] 生成交易信號，資料長度: {len(data)}")
        
        signals = ['BUY'] * len(data)
        print(f"[{self.name}] 生成信號完成，共 {len(signals)} 筆")
        print(f"[{self.name}] 最後 5 筆信號: {signals[-5:]}")
        print(f"[{self.name}] 資料索引: {data.index[-5:]}")
        df = pd.Series(signals, index=data.index)
        print(f"[{self.name}] 信號 DataFrame:\n{df.tail(5)}")
        
        return pd.Series(signals, index=data.index)