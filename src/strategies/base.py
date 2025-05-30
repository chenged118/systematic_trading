# src/strategies/base.py

from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """
    所有交易策略的抽象基底類別
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        根據歷史資料產生交易訊號。
        - data: 包含至少 'close' 欄位的 DataFrame
        - return: pd.Series(['BUY' | 'SELL' | 'HOLD']) 對應每一個 row
        """
        pass