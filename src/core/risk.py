# src/risk.py

class RiskManager:
    def __init__(self, max_drawdown=0.2, max_position_size=0.3):
        self.max_drawdown = max_drawdown
        self.max_position_size = max_position_size

    def check_order(self, current_position, new_order_amount, total_equity):
        """
        根據風控限制檢查是否允許下單
        """
        proposed_total = current_position + new_order_amount
        if proposed_total * 1.0 / total_equity > self.max_position_size:
            print("⚠️ 超過最大倉位限制")
            return False
        return True