# src/executor/simulator.py
import datetime

class Simulator:
    def __init__(self):
        self.cash = 10000
        self.position = 0
        self.avg_entry_price = 0  # 平均進場價
        self.cumulative_pnl = 0
        self.last_buy_price = None  # 用來計算損益

    # def execute_order(self, side, amount, price):
    #     if side == "BUY":
    #         cost = amount * price
    #         if self.cash >= cost:
    #             self.cash -= cost
    #             self.position += amount
    #             print(f"✅ Bought {amount} @ {price}. Cash left: {self.cash}")
    #         else:
    #             print("⚠️ Not enough cash")

    def execute_order(self, side, amount, price):
        order = {
            "timestamp": str(datetime.datetime.now()),
            "side": side,
            "amount": amount,
            "price": price,
            "PNL": 0,
            "Cumulative PNL": self.cumulative_pnl,
            "status": "pending"
        }

        if side == "BUY":
            cost = amount * price
            if self.cash >= cost:
                self.cash -= cost
                self.position += amount
                self.avg_entry_price = price  # 假設每次都買 1 單位，就直接用這個
                self.last_buy_price = price
                order["status"] = "success"
            else:
                order["status"] = "failed"

        elif side == "SELL":
            if self.position >= amount:
                self.position -= amount
                self.cash += amount * price

                # 計算 PNL
                pnl = (price - self.last_buy_price) * amount if self.last_buy_price else 0
                self.cumulative_pnl += pnl

                order["PNL"] = pnl
                order["Cumulative PNL"] = self.cumulative_pnl
                order["status"] = "success"
            else:
                order["status"] = "failed"

        # elif side == "BUY_LIMIT":
        #     # 模擬限價買單
        #     print(f"模擬限價買單：{amount} @ {price}")
        #     if self.cash >= amount * price:
        #         self.cash -= amount * price
        #         self.position += amount
        #     else:
        #         raise ValueError("Not enough cash to execute BUY_LIMIT order.")
        # elif side == "SELL_LIMIT":  
        #     # 模擬限價賣單
        #     print(f"模擬限價賣單：{amount} @ {price}")
        #     if self.position >= amount:
        #         self.position -= amount
        #         self.cash += amount * price
        #     else:
        #         raise ValueError("Not enough position to execute SELL_LIMIT order.")
        # elif side == "BUY_MARKET":
        #     # 模擬市價買單
        #     print(f"模擬市價買單：{amount} @ 市價")
        #     if self.cash >= amount * price:
        #         self.cash -= amount * price
        #         self.position += amount
        #     else:
        #         raise ValueError("Not enough cash to execute BUY_MARKET order.")
        # elif side == "SELL_MARKET":
        #     # 模擬市價賣單
        #     print(f"模擬市價賣單：{amount} @ 市價")
        #     if self.position >= amount:
        #         self.position -= amount
        #         self.cash += amount * price
        #     else:
        #         raise ValueError("Not enough position to execute SELL_MARKET order.")
        
        elif side == "HOLD":
            # 什麼都不做
            order["status"] = "success"

        else:
            raise ValueError("Unknown order type.")

        return order