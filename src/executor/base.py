# src/executor/base.py

from abc import ABC, abstractmethod

class AbstractExecutor(ABC):
    """
    所有交易執行器（模擬、Bybit實盤）都應繼承此抽象類別
    """

    @abstractmethod
    def execute_order(self, side: str, amount: float, price: float) -> dict:
        """
        執行交易動作

        :param side: 'BUY', 'SELL', or 'HOLD'
        :param amount: 數量
        :param price: 價格（模擬用或作為限價參考）
        :return: 一筆交易記錄（字典）
        """
        pass