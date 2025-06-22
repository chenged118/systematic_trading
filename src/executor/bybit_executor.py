# src/executor/bybit_executor.py

import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from pybit.unified_trading import HTTP
from src.executor.base import AbstractExecutor

class BybitExecutor(AbstractExecutor):
    def __init__(self):
        load_dotenv()
        mode = os.getenv("MODE", "test")

        if mode == "test":
            api_key = os.getenv("BYBIT_TEST_API_KEY")
            api_secret = os.getenv("BYBIT_TEST_API_SECRET")
            isTestnet = True
        elif mode == "live":
            api_key = os.getenv("BYBIT_LIVE_API_KEY")
            api_secret = os.getenv("BYBIT_LIVE_API_SECRET")
            isTestnet = False
        else:
            raise ValueError("Unknown MODE setting")

        self.session = HTTP(
            testnet=isTestnet,
            api_key=api_key,
            api_secret=api_secret
        )

    def execute_order(self, side: str, amount: float, price: float):
        try:
            if side == "BUY":
                order = self.session.place_order(
                    category="linear",
                    symbol="BTCUSDT",
                    side="Buy",
                    order_type="Market",
                    qty=amount,
                    time_in_force="GoodTillCancel"
                )
            elif side == "SELL":
                order = self.session.place_order(
                    category="linear",
                    symbol="BTCUSDT",
                    side="Sell",
                    order_type="Market",
                    qty=amount,
                    time_in_force="GoodTillCancel"
                )
            elif side == "HOLD":
                return {
                    "timestamp": str(datetime.datetime.now()),
                    "side": side,
                    "amount": amount,
                    "price": price,
                    "status": "success"
                }
            else:
                raise ValueError("Invalid side")

            return {
                "timestamp": str(datetime.datetime.now()),
                "side": side,
                "amount": amount,
                "price": price,
                "order_id": order["result"]["orderId"],
                "status": "success"
            }

        except Exception as e:
            return {
                "timestamp": str(datetime.datetime.now()),
                "side": side,
                "amount": amount,
                "price": price,
                "status": "failed",
                "error": str(e)
            }
        
    def get_balance(self):
        # 取得帳戶餘額
        return self.session.get_wallet_balance(accountType="UNIFIED")

    def get_trade_history(self, symbol="BTCUSDT", limit=50):
        try:
            response = self.session.get_executions(
                category="spot",  # 'linear' or 'spot' or 'inverse'
                symbol=symbol,
                limit=limit
            )
            trades = response.get("result", {}).get("list", [])
            if not trades:
                return pd.DataFrame()
            
            df = pd.DataFrame(trades)
            df["execTime"] = pd.to_datetime(df["execTime"], unit="ms")
            return df[["execTime", "side", "orderQty", "execPrice", "execValue", "execType", "symbol"]]
        except Exception as e:
            print(f"❌ 無法取得歷史成交紀錄: {e}")
            return pd.DataFrame()
        
    def get_open_orders(self, symbol="BTCUSDT", category="spot", limit=50):
        try:
            response = self.session.get_open_orders(
                category=category,  # "spot" 或 "linear"
                symbol=symbol,
                limit=limit
            )
            orders = response.get("result", {}).get("list", [])
            if not orders:
                return pd.DataFrame()

            df = pd.DataFrame(orders)
            df["createdTime"] = pd.to_datetime(df["createdTime"], unit="ms")
            return df[["orderId", "symbol", "side", "orderType", "qty", "price", "createdTime", "orderStatus"]]
        except Exception as e:
            print(f"❌ 無法取得掛單資訊: {e}")
            return pd.DataFrame()