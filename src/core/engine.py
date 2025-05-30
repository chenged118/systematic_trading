import pandas as pd

class TradingEngine:
    def __init__(self, strategy, executor):
        self.strategy = strategy
        self.executor = executor

    def run(self):
        # 正確的模擬資料格式：DataFrame
        prices = [100, 98, 99, 101, 97]
        data = pd.DataFrame({'close': prices})

        signals = self.strategy.generate_signals(data)

        for i, signal in enumerate(signals):
            if signal == 'BUY':
                self.executor.execute_order("BUY", amount=1, price=data['close'].iloc[i])