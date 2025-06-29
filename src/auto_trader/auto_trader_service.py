# src/auto_trader/auto_trader_service.py

import threading
import time
import pandas as pd
from src.auto_trader.state import state
from src.executor.bybit_executor import BybitExecutor
from src.auto_trader.order_ws import start_ws
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

        # 啟動 WebSocket 訂單監控
        start_ws()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def run_loop(self):
        while self.running:
            try:
                # data = load_market_data("data/live/latest.csv")  # 可以改成串 API
                data = self.fetch_latest_market_data(symbol="BTCUSDT", interval="1", limit=50)
                print(f"[自動交易] 獲取最新市場資料，共 {len(data)} 筆")
                print(data.tail(5))  # 顯示最後 5 筆資料
                signal = self.strategy.generate_signals(data).iloc[-1]
                print(f"[自動交易] 最新交易信號: {signal}")
                last_price = data['close'].iloc[-1]
                print(f"[自動交易] 最新價格: {last_price}")

                print(f"🔔 正在送出訂單：{signal} {last_price} BTC @ 市價")
                if signal == "BUY":
                    self.executor.execute_order("BUY", 0.001, last_price)
                elif signal == "SELL":
                    self.executor.execute_order("SELL", 0.001, last_price) 

                # TODO: 加入停損檢查邏輯
                # 例如持倉虧損超過一定比例就賣出

            except Exception as e:
                import traceback
                print(f"[自動交易錯誤] {e}")
                traceback.print_exc()
            time.sleep(self.interval_sec)

    # TODO: 專案變大時可以抽出做成另一個 class or module 以遵循 SRP
    def fetch_latest_market_data(self, symbol="BTCUSDT", interval="1", limit=50):
        """
        使用 Bybit API 獲取即時市場資料
        :param symbol: 幣種，如 BTCUSDT
        :param interval: K 線週期，"1" 代表 1 分鐘
        :param limit: 回傳筆數
        :return: DataFrame 格式資料
        """
        try:
            response = self.executor.session.get_kline(
                category="linear",  # "linear" 為合約；"spot" 為現貨
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            candles = response["result"]["list"]
            df = pd.DataFrame(candles, columns=[
                "timestamp", "open", "high", "low", "close", "volume", "turnover"
            ])
            df["close"] = df["close"].astype(float)
            return df
        except Exception as e:
            print(f"[錯誤] 獲取市場資料失敗: {e}")
            return pd.DataFrame()