# src/executor/simulator.py

class Simulator:
    def __init__(self):
        self.cash = 10000
        self.position = 0

    def execute_order(self, side, amount, price):
        if side == "BUY":
            cost = amount * price
            if self.cash >= cost:
                self.cash -= cost
                self.position += amount
                print(f"✅ Bought {amount} @ {price}. Cash left: {self.cash}")
            else:
                print("⚠️ Not enough cash")