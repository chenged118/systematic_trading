# src/auto_trader/auto_trader_service.py

import threading
import time
from src.auto_trader.state import state
from src.executor.bybit_executor import BybitExecutor
from src.strategies import get_strategy
from data.loader import load_market_data

class AutoTraderService:
    def __init__(self, strategy_name, stop_loss_pct=0.05, interval_sec=10):
        self.executor = BybitExecutor()
        self.strategy = get_strategy(name=strategy_name)
        self.stop_loss_pct = stop_loss_pct
        self.interval_sec = interval_sec
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_loop)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def run_loop(self):
        while self.running:
            try:
                data = load_market_data("data/live/latest.csv")  # 可以改成串 API
                signal = self.strategy.generate_signals(data)[-1]
                last_price = data['close'].iloc[-1]

                if signal == "BUY":
                    self.executor.execute_order("BUY", 1, last_price)
                elif signal == "SELL":
                    self.executor.execute_order("SELL", 1, last_price)

                # TODO: 加入停損檢查邏輯
                # 例如持倉虧損超過一定比例就賣出

            except Exception as e:
                print(f"[自動交易錯誤] {e}")
            time.sleep(self.interval_sec)