import pandas as pd

from abc import ABC, abstractmethod
from src.executor.base import AbstractExecutor


class TradingEngine:
    def __init__(self, strategy, executor: AbstractExecutor):
        self.strategy = strategy
        self.executor = executor
        self.trades = []

    def run(self, data):
        signals = self.strategy.generate_signals(data)
        for i, signal in enumerate(signals):
            price = data['close'].iloc[i]

            if signal == 'BUY':
                # TODO: 檢查資金是否足夠
                # TODO: 檢查是否已有持倉
                # TODO: 檢查是否符合下單條件
                # TODO: 記錄交易時間
                # TODO: amount 參數化
                result = self.executor.execute_order("BUY", 1, price)
            elif signal == 'SELL':
                result = self.executor.execute_order("SELL", 1, price)
            else:
                result = self.executor.execute_order("HOLD", 0, price)
            
            # 記錄交易結果
            self.trades.append(result)

        self.save_trades_to_csv("reports/trade_log.csv")

    def save_trades_to_csv(self, filepath):
        df = pd.DataFrame(self.trades)
        df.to_csv(filepath, index=False)
        print(f"✅ 已儲存交易紀錄：{filepath}")
